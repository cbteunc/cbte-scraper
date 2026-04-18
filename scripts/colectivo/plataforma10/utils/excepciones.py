import traceback

def get_traceback(e):
  return "".join(traceback.format_exception(type(e), e, e.__traceback__))
