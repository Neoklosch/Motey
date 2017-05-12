from sanic import Blueprint


blueprintendpoint = Blueprint('blueprintendpoint')


@blueprintendpoint.route('/')
async def bp_root(request):
    if request.content_type == 'application/x-yaml':
        result = request.get_data(cache=False, as_text=True)
        print(result)
        return '', 201
    else:
        return None, 400
