import sys
import tkinter
import random

TOT_AIR_POLLUTION_AVG = []
TOT_TEMPERATURE_AVG = []

STD_DEV_TEM_AVG = []
STD_DEV_POL_AVG = []


class Cell:
    def __init__(self, grid, x, y, _type, temperature=25, wind_direction=0, wind_strength=0, air_pollution=0,
                 air_pollution_factor=0.011, cloud_accumulation=0):
        self.grid = grid
        self.x = x
        self.y = y

        self.type = _type  # could be: land/city/forest/sea/iceberg
        self.temperature = temperature  # initial temperature
        self.wind_direction = wind_direction  # Clockwise method [1,12]
        self.wind_strength = wind_strength  # [0,1] 0 means no wind , 1 means max strength wind
        self.air_pollution = air_pollution  # 0 is not polluted at all, 1 is fully polluted.
        self.air_pollution_factor = air_pollution_factor  # cause of air pollution
        self.avg_temperature = -20 if self.type == "iceberg" else 25
        self.cloud_accumulation = cloud_accumulation

        # temp verbs for calculation of the next day's data
        self.next_type = _type
        self.next_temperature = temperature
        self.next_air_pollution = air_pollution
        self.next_air_pollution_factor = air_pollution_factor
        self.next_wind_direction = wind_direction
        self.next_wind_strength = wind_strength
        self.next_cloud_accumulation = cloud_accumulation

    # update next day's data
    def exec(self):
        self.type = self.next_type
        self.temperature = self.next_temperature
        self.wind_direction = self.next_wind_direction
        self.wind_strength = self.next_wind_strength
        self.air_pollution = self.next_air_pollution
        self.cloud_accumulation = self.next_cloud_accumulation

    def calc_next_day(self):

        if self.air_pollution >= 0.7:  # air pollution is high. temperature rise
            if self.temperature < 35:
                self.next_temperature = self.temperature + (self.air_pollution / 2 ** 1)
            elif self.temperature < 70:
                self.next_temperature = self.temperature + (self.air_pollution / 2 ** 3)
            else:
                self.next_temperature = self.temperature + (self.air_pollution / 2 ** 5)

        else:
            # air pollution is low. the temperature is heading towards the average
            if self.temperature > self.avg_temperature:
                self.next_temperature = self.temperature - 0.1
            elif self.temperature < self.avg_temperature:
                self.next_temperature = self.temperature + 0.1

        if self.type == "land":
            # land makes mid-wind level
            self.next_wind_strength = random.uniform(0, 1)
            # in desolate land low chance of rain
            self.next_cloud_accumulation = random.uniform(0, 0.8)

        if self.type == "city":
            # city makes mid-wind level
            self.next_wind_strength = random.uniform(0, 1)
            # in cities mid-chance of rain
            self.next_cloud_accumulation = random.uniform(0.2, 1)
            # city makes air pollution
            self.next_air_pollution = self.next_air_pollution + self.next_air_pollution_factor
            # city dies above 80 degrees
            if self.temperature > 80:
                self.next_type = "land"
            self.normalize("next_air_pollution")

        if self.type == "forest":
            # forest makes low wind level
            self.next_wind_strength = random.uniform(0.2, 1)
            # in the forest high change of rain
            self.next_cloud_accumulation = random.uniform(0.3, 1)
            # if air pollution reach 100% or temp above 60 the forest dies
            if self.next_air_pollution >= 1 or self.temperature >= 60:
                self.next_type = "land"
            else:
                # forest makes oxygen that reduce the pollution
                self.next_air_pollution = self.next_air_pollution - 0.01
                self.normalize("next_air_pollution")

        if self.type == "sea":
            # sea makes high wind level
            self.next_wind_strength = random.uniform(0.3, 1)
            # in the sea high change of rain
            self.next_cloud_accumulation = random.uniform(0.3, 1)
            # when 0 degrees sea becomes ice
            if self.temperature < 0:
                self.next_type = "iceberg"
            # Water evaporates at 100 degrees
            elif self.temperature >= 100:
                self.next_type = "land"

        if self.type == "iceberg":
            # iceberg makes high wind level
            self.next_wind_strength = random.uniform(0.4, 1)
            # in icebergs low chance of rain
            self.next_cloud_accumulation = random.uniform(0, 0.6)
            # ice melt above 0 degrees
            if self.temperature > 0:
                self.next_type = "sea"

        # if the cloud accumulation 0.5 and above we got rain with different intensity, rain that reduce air pollution
        if self.next_cloud_accumulation >= 0.9:  # heavy rain,reduce more air pollution
            self.next_air_pollution = (self.next_air_pollution / 1.6)
            self.next_temperature = self.next_temperature - 0.01
        elif self.next_cloud_accumulation >= 0.7:  # Moderate rain
            self.next_air_pollution = (self.next_air_pollution / 1.4)
            self.next_temperature = self.next_temperature - 0.005
        elif self.next_cloud_accumulation >= 0.5:  # light rain
            self.next_air_pollution = (self.next_air_pollution / 1.2)
            self.next_temperature = self.next_temperature - 0.002
        self.normalize("next_air_pollution")

        # calculate wind effect
        self.next_wind_direction = random.uniform(0, 11.99)  # Determine the direction of the wind
        relevant_pol_neighbours = 1  # to avoid dividing by 0
        relevant_cold_tem_neighbours = 1
        relevant_hot_tem_neighbours = 1
        neighbours_pol_factor = 0
        neighbours_cold_tem_factor = 0
        neighbours_hot_tem_factor = 0
        # all our cell's neighbours in a matrix
        mat = self.grid.get_neighbours(self.x, self.y)
        pivot = 4.5  # initiate state of our pivot
        pivot_range = 1.5
        (i, j) = (0, 0)  # matrix index
        while not (i, j) == (1, 1):  # matrix center == (1,1)
            (_dir, _str, pol, tem) = mat[i][j]
            v = abs(pivot - _dir)  # check the distance of our direction from the pivot center
            if v <= pivot_range:  # if this cell hit as with wind, else not relevant
                relevant_pol_neighbours += 1  # count the neighbours
                # the neighbours wind is on our cell's, this formula calculates wind strength*pollution
                # as a function of proximity to the pivot center
                neighbours_pol_factor += (((pivot_range - v) / pivot_range) * _str * pol)
                # if we got wind from our colder neighbour, we got cooler :)
                if self.temperature >= tem:
                    relevant_cold_tem_neighbours += 1
                    # same principle but with our neighbour's temperature/(main avg tem)
                    neighbours_cold_tem_factor += (
                            ((pivot_range - v) / pivot_range) * _str * abs(tem / self.grid.temperature_avg ** 2))
                # if we got hot wind from out hotter neighbour, we got hotter :(
                else:
                    relevant_hot_tem_neighbours += 1
                    neighbours_hot_tem_factor += (
                            ((pivot_range - v) / pivot_range) * _str * abs(tem / self.grid.temperature_avg ** 3))

            (i, j) = self.next_clock_scan(i, j, len(mat))
            pivot += pivot_range
            if pivot > 12:
                pivot = 1.5

        # update the values divided by num of relevant neighbours
        self.next_air_pollution = self.next_air_pollution + (neighbours_pol_factor / relevant_pol_neighbours)
        self.next_temperature = self.next_temperature - (neighbours_cold_tem_factor / relevant_cold_tem_neighbours)
        self.next_temperature = self.next_temperature + (neighbours_hot_tem_factor / relevant_hot_tem_neighbours)
        self.normalize("next_air_pollution")

    # calculate and return the index scan clock-wise on the matrix
    def next_clock_scan(self, i, j, _len):
        if i == 1 and j == 0:  # end of the clock circle
            return (1, 1)
        else:
            if i == 0 and j < (_len - 1):
                return (i, j + 1)
            elif i < (_len - 1):
                return (i + 1, j)
            elif i == (_len - 1) and j > 0:
                return (i, j - 1)
            elif i > 1:
                return (i - 1, j)

    def get_color(self):
        if self.type == "land":
            return "saddle brown" if (self.temperature < 120) else "red3"
        if self.type == "forest":
            return "forest green" if (self.air_pollution < 0.3) else "olive drab"
        if self.type == "sea":
            return "#1a53ff" if (self.temperature < 40 or self.air_pollution < 0.4) else "RoyalBlue1"
        if self.type == "iceberg":
            return "#FAFAEB"
        if self.type == "city":
            return random.choice(["#FFFF14", "#EEEE12", "#CDCD10"]) if (
                    self.temperature < 55 or self.air_pollution < 0.5) \
                else random.choice(["goldenrod2", "goldenrod3", "goldenrod4"])

    def normalize(self, name):
        value = getattr(self, name)
        if value < 0:
            value = 0
        elif value > 1:
            value = 1

        setattr(self, name, value)


class Grid:
    def __init__(self, length, map_file, air_pollution_factor):
        self.length = length
        self.map_file = map_file
        self.air_pollution_factor = air_pollution_factor
        self.cells = self.create_cells()
        self.day = 1
        self.air_pollution_avg = 0  # init value
        self.temperature_avg = 25  # init value
        self.standard_deviation = 0
        self.T_MAX = (sys.maxsize * -1) - 1
        self.T_MIN = (sys.maxsize)
        self.P_MAX = (sys.maxsize * -1) - 1
        self.P_MIN = (sys.maxsize)

    # get the direct neighbours of index (x,y) in a matrix
    def get_neighbours(self, x, y):
        mat = [
            [
                (self.cells[((x + i) % self.length)][((y + j) % self.length)].__getattribute__("next_wind_direction"),
                 self.cells[((x + i) % self.length)][((y + j) % self.length)].__getattribute__("next_wind_strength"),
                 self.cells[((x + i) % self.length)][((y + j) % self.length)].__getattribute__("next_air_pollution"),
                 self.cells[((x + i) % self.length)][((y + j) % self.length)].__getattribute__("next_temperature"))
                for i in range(-1, 2)] for j in range(-1, 2)]

        return mat

    def exec_new_day(self):
        self.day += 1

        sum_vals_air_pol = 0
        sum_vals_temp = 0
        _sum_std_div_pol = 0
        _sum_std_div_tem = 0
        tot_day_temp_vals = []
        tot_day_pol_vals = []

        for x in range(self.length):
            for y in range(self.length):
                self.cells[x][y].calc_next_day()
                _pol_val = self.cells[x][y].__getattribute__("air_pollution")
                _tmp_val = self.cells[x][y].__getattribute__("temperature")

                sum_vals_air_pol += _pol_val
                sum_vals_temp += _tmp_val

                tot_day_pol_vals.append(_pol_val)
                tot_day_temp_vals.append(_tmp_val)

                if _tmp_val > self.T_MAX:
                    self.T_MAX = _tmp_val
                if _tmp_val < self.T_MIN:
                    self.T_MIN = _tmp_val
                if _pol_val > self.P_MAX:
                    self.P_MAX = _pol_val
                if _pol_val < self.P_MIN:
                    self.P_MIN = _pol_val

        self.air_pollution_avg = sum_vals_air_pol / pow(self.length, 2)
        self.temperature_avg = sum_vals_temp / pow(self.length, 2)

        for x in tot_day_pol_vals:
            _sum_std_div_pol += pow((x - self.air_pollution_avg), 2)

        for y in tot_day_temp_vals:
            _sum_std_div_tem += pow((y - self.temperature_avg), 2)

        # average of standard deviation
        STD_DEV_POL_AVG.append(pow((_sum_std_div_pol / len(tot_day_pol_vals)), 0.5))
        STD_DEV_TEM_AVG.append(pow((_sum_std_div_tem / len(tot_day_temp_vals)), 0.5))

        # average
        TOT_AIR_POLLUTION_AVG.append(self.air_pollution_avg)
        TOT_TEMPERATURE_AVG.append(self.temperature_avg)

        for x in range(self.length):
            for y in range(self.length):
                self.cells[x][y].exec()

    def create_cells(self):
        # create an empty new matrix
        cells = [[0 for i in range(self.length)] for j in range(self.length)]
        map = self.load_map(self.map_file)

        for x in range(self.length):
            for y in range(self.length):
                cells[x][y] = Cell(self, x, y, _type=map[x][y], temperature=random.randint(-25, -15)
                if map[x][y] == "iceberg" else random.randint(20, 30))

        return cells

    def load_map(self, path):
        _map = [[0 for i in range(self.length + 2)] for j in range(self.length + 2)]

        with open(path, 'r') as file:
            for y in range(self.length):
                for x in range(self.length):
                    char = file.read(1)

                    while char not in ['L', 'C', 'F', 'S', 'I']:
                        char = file.read(1)

                    if char == "L":
                        _map[x][y] = "land"
                    if char == "C":
                        _map[x][y] = "city"
                    if char == "F":
                        _map[x][y] = "forest"
                    if char == "S":
                        _map[x][y] = "sea"
                    if char == "I":
                        _map[x][y] = "iceberg"

        return _map


class Auto:
    def __init__(self, length, cell_size, map_file, refresh_rate, deadline=365, air_pollution_factor=0.01):
        self.length = length
        self.cell_size = cell_size
        self.refresh_rate = refresh_rate
        self.deadline = deadline

        self.items = [[0 for i in range(self.length)] for j in range(self.length)]

        self.grid = Grid(self.length, map_file, air_pollution_factor=air_pollution_factor)
        self.root = tkinter.Tk()
        self.root.title("Global warming model - cellular automaton - Tommy Ashkenazi")

        self.label = tkinter.Label(self.root)
        self.label.pack()

        self.canvas = tkinter.Canvas(self.root, width=self.length * self.cell_size, height=self.length * self.cell_size)
        self.canvas.pack()

        self.items = self.update_canvas(self.items)

        self.root.after(self.refresh_rate, self.refresh_window)
        self.root.mainloop()

    def refresh_window(self):
        self.grid.exec_new_day()

        if self.grid.day >= self.deadline:
            self.update_canvas(canvas_items=self.items, canvas_done=True)
            self.label.config(
                text="Day {}                  Avg_temp {}                 Avg_air_pol {}                  FINISHED"
                .format(self.grid.day,
                        round(self.grid.temperature_avg, 3),
                        round(self.grid.air_pollution_avg, 3)))

        else:
            self.update_canvas(canvas_done=True, canvas_items=self.items)
            self.root.after(self.refresh_rate, self.refresh_window)
            self.label.config(
                text="Day {}                  Avg_temp {}                   Avg_air_pol {}"
                .format(self.grid.day,
                        round(self.grid.temperature_avg, 3),
                        round(self.grid.air_pollution_avg, 3)))

    def update_canvas(self, canvas_items, canvas_done=False):
        cell_items = self.grid.cells

        if not canvas_done:
            for x in range(len(cell_items)):
                for y in range(len(cell_items)):
                    cell = cell_items[x][y]

                    cell_txt = int(cell.temperature)
                    rect_id = self.canvas.create_rectangle(x * self.cell_size, y * self.cell_size,
                                                           (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                                                           fill=cell.get_color())
                    txt_id = self.canvas.create_text((x + 0.5) * self.cell_size, (y + 0.5) * self.cell_size,
                                                     text=cell_txt, font="david 9")

                    canvas_items[x][y] = (rect_id, txt_id)

            return canvas_items

        else:
            for x in range(len(canvas_items)):
                for y in range(len(canvas_items)):
                    cell = cell_items[x][y]
                    cell_txt = int(cell.temperature)
                    (rect_id, txt_id) = canvas_items[x][y]
                    self.canvas.itemconfig(rect_id, fill=cell.get_color())
                    self.canvas.itemconfig(txt_id, text=cell_txt)

    def final_avg_calc(self, arr):
        _sum = 0
        for i in arr:
            _sum += i
        return _sum / len(arr)


if __name__ == '__main__':

    auto = Auto(length=50, cell_size=15, refresh_rate=1,
                deadline=365, map_file="my_map.txt", air_pollution_factor=0.01)

    year_tem_avg = auto.final_avg_calc(TOT_TEMPERATURE_AVG)
    year_pol_avg = auto.final_avg_calc(TOT_AIR_POLLUTION_AVG)
    year_tem_std_dev = auto.final_avg_calc(STD_DEV_TEM_AVG)
    year_pol_std_dev = auto.final_avg_calc(STD_DEV_POL_AVG)

    print("TEMPERATURE STATUS -\t\tMax= {:.2f}\tMin= {:.2f}\tAVG= {:.2f}\tStd_dev= {:.2f}".format(
        auto.grid.T_MAX,
        auto.grid.T_MIN,
        year_tem_avg,
        year_tem_std_dev))

    print("AIR POLLUTION STATUS -\t\tMax= {:.2f}\tMin= {:.2f}\tAVG= {:.2f}\tStd_dev= {:.2f}".format(
        auto.grid.P_MAX,
        auto.grid.P_MIN,
        year_pol_avg,
        year_pol_std_dev))

    file1 = open("stn_temperature.txt", 'w')
    file2 = open("temperature.txt", 'w')
    for i in TOT_TEMPERATURE_AVG:
        file2.write("{}\n".format(i))
        if not (year_tem_std_dev == 0):
            file1.write("{}\n".format((i - year_tem_avg) / year_tem_std_dev))
    file1.close()
    file2.close()

    file1 = open("stn_air_pollution.txt", 'w')
    file2 = open("air_pollution.txt", 'w')
    for i in TOT_AIR_POLLUTION_AVG:
        file2.write("{}\n".format(i))
        if not (year_pol_std_dev == 0):
            file1.write("{}\n".format((i - year_pol_avg) / year_pol_std_dev))
    file1.close()
    file2.close()
