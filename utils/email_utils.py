import re


def is_valid_email(email: str) -> bool:
    """
    Validate an email address using a regular expression.

    Args:
    email (str): The email address to validate.

    Returns:
    bool: True if the email address matches the pattern, False otherwise.

    This function checks if the given email address conforms to a basic pattern indicating a
    valid format (i.e., something like 'example@domain.com'). It ensures that the email starts
    with alphanumeric characters (including dots), followed by an '@' symbol, and ends with a
    domain name that includes one or more dots. The domain extension must be at least two characters long.
    """

    pattern = r'^[a-zA-Z0-9.]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$'

    return re.match(pattern, email) is not None


def attach_file(message, filepath: str) -> str:

    """
    Attach a file to an email message.

    Args:
    message (MIMEMultipart): The email message object to which the file will be attached.
    filepath (str): The path to the file that needs to be attached.

    Returns:
    str: A success message indicating the file was attached successfully.

    Raises:
    IOError: An error if the file cannot be read or attached to the email.

    This function attempts to open a file in binary read mode and attaches it to the provided
    email message object as a MIMEBase part. It encodes the file's content in base64 and sets
    the appropriate content disposition header using the filename. If the operation fails for any reason
    (like the file not being found, or issues with reading the file), it raises an IOError with
    an error message detailing the specific issue.
    """

    from email.mime.base import MIMEBase
    from email import encoders

    try:
        part = MIMEBase(
            'application',
            'octet-stream',
        )
        with open(filepath, 'rb') as file:
            part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f"attachment; filename={filepath.split('/')[-1]}"
            )
            message.attach(part)
        return "Your file/files attached successfully."
    except Exception as e:
        raise IOError(f"Failed to attach file: {filepath}. Error: {e}")
