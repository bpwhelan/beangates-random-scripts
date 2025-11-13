import sqlite3
import random
import time
import datetime
import os

# --- Configuration ---
# IMPORTANT: Replace with the actual path to your Anki collection.anki2 file
# You can usually find this in your Anki profile folder.
# Example path on Windows: C:\Users\YourUsername\AppData\Roaming\Anki2\YourProfileName\collection.anki2
# Example path on macOS: ~/Library/Application Support/Anki2/YourProfileName/collection.anki2
# Example path on Linux: ~/.local/share/Anki2/YourProfileName/collection.anki2
ANKI_DB_PATH = r'C:\Users\Beangate\AppData\Roaming\Anki2\User 1\collection.anki2'

# --- Review Simulation Parameters ---
# These values simulate a 'Good' review (ease=3)
REVIEW_EASE = 3  # 1:Again, 2:Hard, 3:Good, 4:Easy
REVIEW_TYPE = 0  # 0:Learn, 1:Review, 2:Relearn, 3:Filtered/Rescheduled
REVIEW_TIME_MS = 5000 # Simulated time taken to review in milliseconds (e.g., 5 seconds)
# Note: Interval and ease factor might need more complex logic for realistic simulation
# For simplicity, we'll use placeholder values or let Anki recalculate on next sync/review.
SIMULATED_INTERVAL = 1 # Placeholder interval (e.g., 1 day)
SIMULATED_LAST_INTERVAL = 0 # Placeholder last interval
SIMULATED_FACTOR = 2500 # Placeholder ease factor (2500 = 250%)
DRY_RUN = False # Set to True to only print the SQL without executing it
CARD_ID = 1747433461669 # Only if you want to target a specific card, otherwise set to None
# DATE_OVERRIDE = "2025-04-21" # Set to a specific date string 'YYYY-MM-DD' if needed, otherwise None
DATE_OVERRIDE = None

# --- Don't modify below this line unless you know what you're doing ---

def add_review_to_random_suspended_card(db_path):
    """
    Connects to the Anki DB, finds a random suspended card, and adds a review log entry for yesterday.
    """
    if not os.path.exists(db_path):
        print(f"Error: Database file not found at {db_path}")
        return

    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        if CARD_ID:
            random_card_id = CARD_ID
            print(f"Using specified card ID: {random_card_id}")
        else:
            # Find all suspended card IDs in "Sentence Mining" deck
            # queue = -1 means suspended
            cursor.execute("SELECT id FROM cards WHERE queue = -1 AND did IN (SELECT id FROM decks WHERE name = 'Sentence Mining' COLLATE BINARY)")
            suspended_card_ids = [row[0] for row in cursor.fetchall()]

            print(suspended_card_ids)

            if not suspended_card_ids:
                print("No suspended cards found.")
                return

            # Select a random suspended card ID
            random_card_id = random.choice(suspended_card_ids)
            print(f"Selected random suspended card ID: {random_card_id}")

        if DATE_OVERRIDE:
            try:
                override_date = datetime.datetime.strptime(DATE_OVERRIDE, "%Y-%m-%d")
                override_date = override_date.replace(hour=12, minute=0, second=0, microsecond=0)  # Set to noon to avoid timezone issues
                yesterday_timestamp_ms = int(override_date.timestamp() * 1000)
                print(f"Using overridden date: {DATE_OVERRIDE} (timestamp ms: {yesterday_timestamp_ms})")
            except ValueError:
                print("Invalid DATE_OVERRIDE format. Use 'YYYY-MM-DD'. Falling back to yesterday.")
        else:
            # Calculate timestamp for yesterday
            yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
            # Anki uses milliseconds since the Unix epoch for revlog id
            # and seconds since the Unix epoch for other timestamps (like cards.mod)
            # revlog.id is actually milliseconds since epoch
            yesterday_timestamp_ms = int(yesterday.timestamp() * 1000)

        # Get current max revlog id to ensure uniqueness (though timestamp should be unique enough)
        # Anki's revlog.id is the timestamp, which should be unique for each review.
        # Using the calculated timestamp for yesterday is the correct approach for revlog.id.
        revlog_id = yesterday_timestamp_ms

        # Get a unique update sequence number (usn)
        # Anki uses usn to track changes for syncing.
        # -1 is typically used for manual changes outside of normal sync operations.
        usn = -1

        # Insert a new entry into the revlog table
        # revlog schema: id, cid, usn, ease, ivl, lastIvl, factor, time, type
        # id: milliseconds since epoch
        # cid: card id
        # usn: update sequence number (-1 for manual changes)
        # ease: 1=again, 2=hard, 3=good, 4=easy
        # ivl: interval in days (or seconds for learning cards)
        # lastIvl: last interval in days
        # factor: ease factor in permille (e.g., 2500 for 250%)
        # time: time taken to answer in ms
        # type: 0=learn, 1=review, 2=relearn, 3=filtered/rescheduled
        if DRY_RUN:
            print(f"""
                INSERT INTO revlog (id, cid, usn, ease, ivl, lastIvl, factor, time, type)
                VALUES ({revlog_id}, {random_card_id}, {usn}, {REVIEW_EASE}, {SIMULATED_INTERVAL}, 
                        {SIMULATED_LAST_INTERVAL}, {SIMULATED_FACTOR}, {REVIEW_TIME_MS}, {REVIEW_TYPE})
            """)
        else:
            input("Press Enter to confirm adding the review log entry...")
            cursor.execute("""
                INSERT INTO revlog (id, cid, usn, ease, ivl, lastIvl, factor, time, type)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (revlog_id, random_card_id, usn, REVIEW_EASE, SIMULATED_INTERVAL,
                  SIMULATED_LAST_INTERVAL, SIMULATED_FACTOR, REVIEW_TIME_MS, REVIEW_TYPE))
            conn.commit()
            print(f"Successfully added a review log entry for card {random_card_id} dated yesterday.")



        # Note: This script *only* adds a revlog entry. It does NOT change the card's state (e.g., un-suspend it).
        # The card will remain suspended, but it will have a review history entry from yesterday.
        # If you wanted to un-suspend it, you would need to update the 'queue' and other fields in the 'cards' table.
        # Example to un-suspend:
        # cursor.execute("UPDATE cards SET queue = 2, mod = ?, usn = ? WHERE id = ?", (int(time.time()), usn, random_card_id))
        # However, the request was just to add a review log, not un-suspend.


    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

# --- Main execution ---
if __name__ == "__main__":
    print("Attempting to add a review to a random suspended card...")
    add_review_to_random_suspended_card(ANKI_DB_PATH)
    print("Script finished.")
