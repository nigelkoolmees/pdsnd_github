# Programming for Data Science with Python: An Udacity Project

import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
            'new york city': 'new_york_city.csv',
            'washington': 'washington.csv',}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('\nHello! Let\'s explore some US bikeshare data!')

    # The while loop below iterates through the entered city and lowers it to accept all inputs.

    while True:
      city = input("\nWould you like to filter by the city Chicago, New York City or Washington?\n").lower()
      if city not in ("chicago", "new york city", "washington"):
        print("Sorry, this city is not available. Please pick between: Chicago, New York City or Washington")
        continue
      else:
        break

    # The while loop iterates through the entered month and makes the input a title to accept all inputs.

    while True:
      month = input("\nChoose a month you would like to filter by: January, February, March, April, May, June. \nOr choose 'All' if you do not want to filter by month.\n").title()
      if month not in ("January", "February", "March", "April", "May", "June", "All"):
        print("Too bad, this month isn't available. Please try again.")
        continue
      else:
        break

    # The while loop iterates through the entered day and makes the input a title to accept all inputs.

    while True:
      day = input("\nWould you like to filter by a specific day? \nPlease enter one of the following: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday. \nOr choose 'All' to get all days.\n").title()
      if day not in ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "All"):
        print("Please try again.")
        continue
      else:
        break

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # Using pandas read_csv function to get the city data as dataframe
    df = pd.read_csv(CITY_DATA[city])

    # Converting the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extracting month and day of week from Start Time to create new columns

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # Filter by month if chosen for

    if month != "All":
        months = ["January", "February", "March", "April", "May", "June"]
        month = months.index(month) + 1

        # Creating a new dataframe when filtered by month
        df = df[df['month'] == month]

    # Filter by day of week if chosen for
    if day != "All":
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Prints the most common month of travel through the dataframe.
    most_common_month = df['month'].mode()[0]
    print('Most common month: ', most_common_month)

    # Prints the most common day of travel through the dataframe.
    most_common_day = df['day_of_week'].mode()[0]
    print('Most common day: ', most_common_day)

    # Prints the most common hour of travel through the dataframe.
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    print('Most common hour: ', most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Prints the most commonly used start station with a count and idmax function.
    start_station = df['Start Station'].value_counts().idxmax()
    print('\nMost commonly used start station: {}'.format(start_station))

    # Prints the most commonly used end station with a count and idmax function.
    end_station = df['End Station'].value_counts().idxmax()
    print('\nMost commonly used end station: {}'.format(end_station))

    # Prints the most frequent combination between start and end station.
    df['Combination'] = df['Start Station']+" "+"to"+" "+df['End Station']
    combi_station = df['Combination'].mode()[0]
    print('\nMost frequent combination of start station and end station: {}'.format(combi_station))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Prints the total travel time in hours, minutes and seconds.

    total_travel_time = df['Trip Duration'].sum()
    minutes, seconds = divmod(total_travel_time, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    weeks, days = divmod(days, 7)
    print("The total trip duration: {} day(s) {} hour(s) {} minute(s) {} second(s)".format(days,hours,minutes,seconds))

    # Prints the mean travel time in minutes and seconds.

    mean_travel_time = round(df['Trip Duration'].mean())
    m,sec = divmod(mean_travel_time,60)
    if m>60:
        h,m = divmod(m,60)
        print("The total trip duration: {} hour(s) {} minute(s) {} second(s)".format(h,m,sec))
    else:
        print("The total trip duration: {} minute(s) {} second(s)".format(m,sec))



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Prints the user count types between customer or subscriber.

    user_types = df['User Type'].value_counts()
    print("User types:\n",user_types)

    # Prints the count of males and females who used the service

    try:
      gender_count = df['Gender'].value_counts()
      print("\nGender count:\n",gender_count)
    except KeyError:
      print("\nGender count: No data available for this month.")

    """ Below a try function get the most common birth dates
        First the earliest birth year or the most oldest person gets printed.
        Then the most recent birth year and lastly the most common birth year."""

    try:
      oldest_age = df['Birth Year'].min()
      print("\nBirth date of oldest person who rode a bike: ", oldest_age)
    except KeyError:
      print("\nBirth date of oldest person: No data available for this month.")

    try:
      most_recent_age = df['Birth Year'].max()
      print("\nBirth date of youngest person who rode a bike: ", most_recent_age)
    except KeyError:
      print("\nBirth date of youngest person who rode a bike: No data available for this month.")

    try:
      most_common_age = df['Birth Year'].value_counts().idxmax()
      print("\nMost common birth year: ", most_common_age)
    except KeyError:
      print("\nMost common birth year: No data available for this month.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    """
    Below a function asks if the user wants to see the entries per 5 rows.
    If the user chooses yes they will see 5 entries and gets asked if they want to see 5 more.
    If selected 'no' the while loop will stop.

    """

def display_data(df):

    while True:
        response=['yes','no']
        choice= input("Would you like to view individual trip data (5 entries)? Type 'yes' or 'no'\n").lower()
        if choice in response:
            if choice=='yes':
                start=0
                end=5
                data = df.iloc[start:end,:9]
                print(data)
            break
        else:
            print("Please enter a valid response")
    if  choice=='yes':
            while True:
                choice_2= input("Would you like to view more trip data? Type 'yes' or 'no'\n").lower()
                if choice_2 in response:
                    if choice_2=='yes':
                        start+=5
                        end+=5
                        data = df.iloc[start:end,:9]
                        print(data)
                    else:
                        break
                else:
                    print("Please enter a valid response")


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
