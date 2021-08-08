
def count_tweets_classified(df, march_type):
    
    count = 0

    for index, row in df.iterrows():

        if row['textclassifierjson']['POSITIVE'] > float(0.7):

            if row['classified_march'] == march_type:

                count += 1
        
    return count


def count_tweets(df, march_type):
    
    count = 0

    for index, row in df.iterrows():

        if row['classified_march'] == march_type:

            count += 1

    return count