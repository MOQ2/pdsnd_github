import time
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def display_raw_data(df):
    """ Display raw data of the dataframe , 5 rows at a time """
    row_index=0 
    while True : 
        keep_displaying = input("Do you want to display 5 rows of raw data? Enter yes or no: ").lower()
        if keep_displaying == 'yes':
            print(df.iloc[row_index:row_index+5])
            row_index += 5
        else:
            break
    


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
    while True:
        city = input("Enter the city name: ").lower()
        if city in CITY_DATA:
            break
        else:
            print("Invalid city name. Please enter a valid city name from chicago, new york city, washington")
        

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Enter the month name: ").lower()
        if month in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
            break
        else:
            print("Invalid month name. Please enter a valid month name from january to june or all")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Enter the day name: ").lower()
        if day in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            break
        else:
            print("Invalid day name. Please enter a valid day name")


    print('-'*40)
    return city, month, day


def load_data(city:str, month:str, day:str):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
        
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
        
        

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # the mode() function returns a Series with the most frequent value
    # display the most common month
    
    common_month = df['month'].mode()[0]
    print('Most Common Month:', common_month)

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('Most Common Day:', common_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('Most Common Hour:', common_hour)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start =  df['Start Station'].mode()[0]
    print('Most Common Start Station:', common_start)

    # display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print('Most Common End Station:', common_end)

    # display most frequent combination of start station and end station trip
    # this adds a new column to the dataframe that concatenates the start and end stations , another way is to use groupby
    df['Start End'] = df['Start Station'] + ' to ' + df['End Station']
    common_start_end = df['Start End'].mode()[0]
    print('Most Common Start-End Station:', common_start_end)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = df['Trip Duration'].sum()
    print('Total Travel Time:', total_travel )

    # display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print('Mean Travel Time:', mean_travel)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df , city:str):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    
    user_types = df['User Type'].value_counts().to_string()
    print('User Types:\n',user_types)
    print('\n')


    # check if city NYC or Chicago
    if city in ['new york city', 'chicago']:
        # Display counts of gender (avaliable for NYC and Chicago)
        gender_count = df.dropna(subset=['Gender']).groupby('Gender').size().to_string()
        print('Gender Count:\n',gender_count)
        print('\n')

        # Display earliest, most recent, and most common year of birth (avaliable for NYC and Chicago)
        
        earliest_birth = df['Birth Year'].min()
        print('Earliest Birth Year:', earliest_birth)
        
        recent_birth = df['Birth Year'].max()
        print('Most Recent Birth Year:', recent_birth)
        
        common_birth = df['Birth Year'].mode()[0]
        print('Most Common Birth Year:', common_birth)
        print('\n')
        
        
    else:
        print ("Unfortunately, Gender count not ablicable for Washington city")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    try :
        while True:
            print("\nNote: Feel free to terminate the program at any time by pressing Ctrl+C\n")
            city, month, day = get_filters()
            try :
                df = load_data(city, month, day)
            except Exception as e:
                print("Error loading data: ", e)
                print("Please check the file path and file name")
                continue
            # Display raw data 5 rows at a time untill user wants to stop or end of data
            display_raw_data(df)
            # Display statistics on data 
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df, city)
            

            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() != 'yes':
                break
            
        print ("\n\nThank you for using the program\n")
        
    except KeyboardInterrupt:
        print("\n\nProgram terminated by user")
        print ("Thank you for using the program")

if __name__ == "__main__":
	main()
