import time
import pandas as pd
import numpy as np

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York': 'new_york_city.csv',
              'Washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    valid_cities = ['Chicago', 'New York', 'Washington']
    valid = True
    while valid:
        city = str(input("Would you like to see data for Chicago, New York, or Washington?: ")).title()
        if city in valid_cities:
            valid = False
        else:
            print("City Name entered is not valid...")

    # get user input for month (all, january, february, ... , june)
    valid_months = ['All', 'January', 'February', 'March', 'April', 'May', 'June']
    valid = True
    while valid:
        month = str(input('Which month - January, February, March, April, May, June, or All?: ')).title()
        if month in valid_months: 
            valid = False
        else:
            print("Month Name entered is not valid...")


    # get user input for day of week (all, monday, tuesday, ... sunday)
    valid_days = ['All', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    valid = True
    while valid:
        day = str(input('Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or All?: ')).title()
        if day in valid_days: 
            valid = False
        else:
            print("Day Name entered is not valid...")


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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'All':
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # display the most common month
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]
    print('Most Popular Start month:', popular_month)

    # display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.day_name()
    popular_day_of_week = df['day_of_week'].mode()[0]
    print('Most Popular Start day of week:', popular_day_of_week)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    Start_Station = df['Start Station'].mode()[0]
    print('Most commonly used start station:', Start_Station)

    # display most commonly used end station
    End_Station = df['End Station'].mode()[0]
    print('Most commonly used end station:', End_Station)

    # display most frequent combination of start station and end station trip
    trip_series = df["Start Station"] + " to " + df["End Station"]
    most_popular_trip = trip_series.describe()["top"]
    print('Most frequent combination of start station and end station trip: ', most_popular_trip)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time: ',total_travel_time)


    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time: ',mean_travel_time)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)


    if 'Gender' in df.columns :
        # Display counts of gender
        genders = df['Gender'].value_counts()
        print(genders)
        
    if 'Birth Year' in df.columns:
        # Display earliest, most recent, and most common year of birth
        earliest_birth_year = int(df['Birth Year'].min())
        print('Earliest birth year: ',earliest_birth_year)
        most_recent_birth_year = int(df['Birth Year'].max())
        print('Most recent birth year: ',most_recent_birth_year)
        most_common_birth_year = int(df['Birth Year'].mode()[0])
        print('Most common birth year: ',most_common_birth_year)

    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """Ask the user if he wants to see the raw data and print 5 rows at time"""
    raw = input('\nWould you like to see raw data? Enter Yes or No\n')
    if raw.title() == 'Yes':
        row = 0
        while True:
            print(df.iloc[row: row+5])
            row += 5
            again = input('\nWould you like to view next five row of raw data? Enter Yes or No\n')
            if again.title() != 'Yes':
                break    
    

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)
       
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
