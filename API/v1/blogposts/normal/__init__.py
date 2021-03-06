import json
import traceback

import aiofiles
import aiohttp
import sanic
import sanic.response



async def handler(req):
    lang = 'en'
    for i in req.query_args:
        if i[0] == 'lang':
            lang = str(i[1])
    async with aiohttp.ClientSession() as ses:
        async with ses.get(
                f'https://www.epicgames.com/fortnite/api/blog/getPosts?category=&postsPerPage=9999&offset=0&locale={lang}&rootPageSlug=blog') as req:
            if req.status != 200:
                try:
                    data = (
                        json.loads(await (await aiofiles.open(f'Cache/blogbosts_normal_{lang}.json', mode='r')).read()))
                except:
                    traceback.print_exc()
                    return sanic.response.json({'status': 500, 'message': 'Intern Server error'}, status=500)
            else:
                data = (await req.json())
    response = {
        'status': 200,
        'message': 'Everything should work fine',
        'data': {
            'blogposts': []
        }
    }

    try:
        for bloglist in data['blogList']:
            temp = {}
            try:
                temp['title'] = bloglist['title']
            except:
                pass
            try:
                temp['description'] = bloglist['shareDescription']
            except:
                pass
            try:
                temp['author'] = bloglist['author']
            except:
                pass
            try:
                temp['url'] = f'https://www.epicgames.com/fortnite{bloglist["urlPattern"]}'
            except:
                pass
            try:
                temp['image'] = bloglist['image']
            except:
                try:
                    temp['image'] = bloglist['trendingImage']
                except:
                    pass
            try:
                temp['date'] = bloglist['date']
            except:
                pass
            response['data']['blogposts'].append(temp)
    except:
        traceback.print_exc()

    try:
        await (await aiofiles.open(f'Cache/blogbosts_normal_{lang}.json', mode='w+', encoding='utf8')).write(
            json.dumps(data, indent=3))
    except:
        traceback.print_exc()

    return sanic.response.json(response)
