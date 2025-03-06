from src.core.repositories.learnerRepo import get_connection, return_connection
from src.core.services.mapper.learnerMapper import map_learners


class LearnerServices:
    def __init__(self):
        # Initializes the LearnerRepository instance
        self.conn = None
        self.cur = None

    def get_all_learners(self):
        try:
            # Get a connection from the pool
            self.conn = get_connection()

            # Create a cursor object
            self.cur = self.conn.cursor()

            # Execute SQL command to fetch all records from the learners table
            self.cur.execute('SELECT * FROM learner;')
            learners = self.cur.fetchall()  # Retrieve all records

            # Return the results
            return learners

        except Exception as e:
            print(f"Error: {e}")
            return []

        finally:
            # Close the cursor and return the connection to the pool
            if self.cur:
                self.cur.close()
            if self.conn:
                return_connection(self.conn)

    def get_learner_by_email(self, email):
        try:
            # Get a connection from the pool
            self.conn = get_connection()

            # Create a cursor object
            self.cur = self.conn.cursor()

            # Execute SQL command to fetch a learner by email
            self.cur.execute('SELECT * FROM learner WHERE email = %s;', (email,))
            learner = self.cur.fetchone()  # Retrieve the single record

            # If learner is found, return the result, otherwise return None
            return learner if learner else None

        except Exception as e:
            print(f"Error: {e}")
            return None

        finally:
            # Close the cursor and return the connection to the pool
            if self.cur:
                self.cur.close()
            if self.conn:
                return_connection(self.conn)

    def get_learner_learning_styles(self, email):
        # Importing map_learners inside the method to avoid circular import
        from src.core.services.mapper.learnerMapper import map_learners

        # Retrieve learner by email
        learner_data = self.get_learner_by_email(email)
        if learner_data:
            # Map learner data (assuming map_learners returns a list of dicts)
            mapped_learners = map_learners([learner_data])
            for learner in mapped_learners:
                # Retrieve all 4 learning styles (LS1 to LS4)
                LS1 = learner.get('LS1', None)  # learning_style_active_reflective
                LS2 = learner.get('LS2', None)  # learning_style_visual_verbal
                LS3 = learner.get('LS3', None)  # learning_style_sensing_intuitive
                LS4 = learner.get('LS4', None)  # learning_style_sequential_global

                # Return all 4 learning styles as a dictionary or tuple
                return {'LS1': LS1, 'LS2': LS2, 'LS3': LS3, 'LS4': LS4}
        return None

# Test the service method
# if __name__ == "__main__":
#     LearnerServicesOBJ = LearnerServices()
#     email_to_search = 'tarek@example.com'
#
#     # Get the learning styles (LS1 to LS4) directly
#     learning_styles = LearnerServicesOBJ.get_learner_learning_styles(email_to_search)
#
#     if learning_styles:
#         print(f"Learning Styles for {email_to_search}:")
#         print(f"LS1 (Active/Reflective): {learning_styles['LS1']}")
#         print(f"LS2 (Visual/Verbal): {learning_styles['LS2']}")
#         print(f"LS3 (Sensing/Intuitive): {learning_styles['LS3']}")
#         print(f"LS4 (Sequential/Global): {learning_styles['LS4']}")
#     else:
#         print(f"Learning Style not found for {email_to_search}")
