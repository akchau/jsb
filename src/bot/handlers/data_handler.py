
async def parse_data(update):
    query = update.callback_query
    data = query.data
    if len(data.split("/")) > 2:
        return data.split("/")[1:]
    if len(data.split("/")) == 2:
        return data.split("/")[1]
    if len(data.split("/")) == 1:
        return None


async def create_data(handler, *args):
    return f"{handler}/" + "/".join(args)
