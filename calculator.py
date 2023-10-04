import matplotlib.pyplot as plt
#from matplotlib import font_manager

#font_path = '/content/drive/Shareddrives/Work Hub/6. Communications/3. Brand guide and templates/0. Refer/Public Sans Font/PublicSans-Light.ttf'  # Replace with the actual file path
#custom_font = font_manager.FontProperties(fname=font_path)

class Calculator:
    def __init__(self):
        self.daily_regular_limit = 9
        self.days_in_week = 6
        self.rest_duration = 0.5  # duration of rest assumed to be 0.5 hours
        self.max_period_before_rest = 5  # continuous hours of work before a rest interval assumed to be 5 hours
        self.total_rest = 1  # Initialize total_rest attribute

    def plot_section(self, start_time, duration, color, label=None):
        """Helper function to plot a section of the bar."""
        if label:
            plt.fill_betweenx([0, 0.5], start_time, start_time + duration, color=color, alpha=1, label=label)
        else:
            plt.fill_betweenx([0, 0.5], start_time, start_time + duration, color=color, alpha=1)
        return start_time + duration  # Return the end time of the section
    

    def calculate(self):
        overtime_total = 0
        results = {}
        if self.weekly_regular_limit % self.days_in_week == 0:
            for day in range(1, self.days_in_week + 1):
                if self.weekly_regular_limit // self.days_in_week <= 9:
                    daily_regular_hours = self.weekly_regular_limit / self.days_in_week  # Use floating-point division
                else:
                    daily_regular_hours = 9
                overtime_hours = self.daily_spread_over_limit - daily_regular_hours - self.total_rest
                self.plot_work_hours(day, daily_regular_hours, overtime_hours, self.total_rest)
                overtime_total += overtime_hours
        else:
            results["Note"] = "Weekly hours are not evenly distributed across all days."
            for day in range(1, self.days_in_week + 1):
                if self.weekly_regular_limit <= 54:
                    if day < 6:
                        daily_regular_hours = self.daily_regular_limit
                    else:
                        daily_regular_hours = self.weekly_regular_limit % self.daily_regular_limit
                else:
                    daily_regular_hours = self.daily_regular_limit
                overtime_hours = self.daily_spread_over_limit - daily_regular_hours - self.total_rest
                self.plot_work_hours(day, daily_regular_hours, overtime_hours, self.total_rest)
                overtime_total += overtime_hours

        present_weekly_regular_hours = 48  # Present regular hours limit

        weekly_regular_earning_present = "{:.2f}".format(present_weekly_regular_hours * 43.11)
        weekly_overtime_earning_present = "{:.2f}".format(12 * 86.22)
        weekly_regular_earning_relaxed = "{:.2f}".format(self.weekly_regular_limit * 43.11)
        weekly_overtime_earning_relaxed = "{:.2f}".format(overtime_total * 86.22)

        results["Overtime Total"] = overtime_total
        results["Present Reg Hour Earnings"] = weekly_regular_earning_present
        results["Present Overtime Hour Earnings"] = weekly_overtime_earning_present
        results["Relaxed Reg Hour Earnings"] = weekly_regular_earning_relaxed
        results["Relaxed Overtime Hour Earnings"] = weekly_overtime_earning_relaxed

        return results

    def plot_work_hours(self, day, daily_regular_hours, overtime_hours, total_rest):
        total_hours = daily_regular_hours + overtime_hours + total_rest
        plt.figure(figsize=(12, 1))
        plt.yticks([])
        plt.title(f"Day {day}")
        ax = plt.gca()
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        plt.xlabel("Hours")
        x_ticks = list(range(0, int(total_hours) + 1))
        plt.xticks(x_ticks)
        plt.xlim(left=0, right=total_hours, emit=True)

        regular_color = '#D8DFF3'
        overtime_color = '#D1F5D3'
        rest_color = '#EF958E'

        time = 0
        labels_added = {'Regular': False, 'Overtime': False, 'Rest': False}

        while time < total_hours:
            regular_shift_one = min(daily_regular_hours, self.max_period_before_rest)
            rest_duration_one = self.rest_duration
            regular_shift_two = daily_regular_hours - regular_shift_one
            overtime_hours_one = self.max_period_before_rest - regular_shift_two if regular_shift_one + regular_shift_two == daily_regular_hours else 0
            overtime_misc = self.max_period_before_rest - regular_shift_one if regular_shift_one < 5 else 0
            rest_duration_two = self.rest_duration
            overtime_hours_two = min((overtime_hours - overtime_hours_one), self.max_period_before_rest)
            
            label = 'Regular' if not labels_added['Regular'] else None
            time = self.plot_section(time, regular_shift_one, regular_color, label)
            labels_added['Regular'] = True

            if regular_shift_one == self.max_period_before_rest:
                label = 'Rest' if not labels_added['Rest'] else None
                time = self.plot_section(time, rest_duration_one, rest_color, label)
                labels_added['Rest'] = True
            else:
                label = 'Overtime' if not labels_added['Overtime'] else None
                time = self.plot_section(time, overtime_misc, overtime_color, label)
                labels_added['Overtime'] = True

            if overtime_misc != 0:
                label = 'Rest' if not labels_added['Rest'] else None
                time = self.plot_section(time, rest_duration_one, rest_color, label)
                labels_added['Rest'] = True
            else:
                time = self.plot_section(time, regular_shift_two, regular_color)
            
            time = self.plot_section(time, overtime_hours_one, overtime_color)
            
            label = 'Rest' if not labels_added['Rest'] else None
            time = self.plot_section(time, rest_duration_two, rest_color, label)
            labels_added['Rest'] = True
            
            if overtime_hours_two > 0:
                time = self.plot_section(time, overtime_hours_two, overtime_color)
        
        plt.xlabel("Hours")

        import streamlit as st
        st.pyplot(plt)
