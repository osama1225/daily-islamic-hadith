from datetime import date
from flask import render_template, request
from hadith_app.routes.helper.request_helper import get_user_agent
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_template_response(r: request, result: dict | None, home_page: bool):
    if result.get('hadith') is not None:
        return render_template("index.html",
                               home_page=home_page,
                               hadith=result.get('hadith'),
                               ua=get_user_agent(r),
                               copyright_year=date.today().year)
    else:
        return (render_template("index.html",
                                home_page=home_page,
                                error=result.get('error'),
                                copyright_year=date.today().year)
                , result.get('status_code'))


def handle_fetch_hadith_success(hadith: dict | None):
    if hadith is not None:
        return {"hadith": hadith, "status_code": 200}
    return handle_fetch_hadith_error(KeyError("Hadith not found"))


def handle_fetch_hadith_error(error: Exception):
    match error:
        case ValueError() as ve:
            logger.error(f"Value error: {ve}")
            error_message = "Something went wrong"
            status_code = 400
        case KeyError() as ke:
            logger.error(f"Key error: {ke}")
            error_message = "Hadith not found"
            status_code = 404
        case Exception() as e:
            logger.error(f"Error fetching hadith: {e}")
            error_message = "Something went wrong. Please try again later."
            status_code = 500
        case _:
            logger.error(f"Error fetching hadith: {error}")
            error_message = "Something went wrong. Please try again later."
            status_code = 500
    return {"error": error_message, "status_code": status_code}
