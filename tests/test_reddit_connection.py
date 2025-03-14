import os
import dotenv
from reddit import get_submissions_text, initialize_reddit_api



def test_submission_returns ():
    # setup api authentication
    dotenv.load_dotenv()
    CLIENT_ID = os.environ.get("CLIENT_ID")
    CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
    reddit_connection = initialize_reddit_api(CLIENT_ID, CLIENT_SECRET)

    SUBMISSION_COUNT = 5
    result = get_submissions_text (reddit_connection, "all", "new", SUBMISSION_COUNT)
    assert result is not None
    assert isinstance (result, list)
    assert len (result) == SUBMISSION_COUNT