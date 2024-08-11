from pixivpy3 import AppPixivAPI
from flask import Flask, jsonify

app = Flask(__name__)

_REFRESH_TOKEN = 'adc63cnv2iAkPdlgg-ApXej0pxeqKuAF0QjX8gvHmSM'

api = AppPixivAPI()
api.auth(refresh_token=_REFRESH_TOKEN)


@app.route('/', methods=['GET'])
def index():
    try:
        json_result = api.search_novel(
            word='Rias Gremory', search_target='keyword', sort='date_desc', start_date=None, end_date=None)

        # json_result = api.webview_novel(22725727)
        # json_result = api.novel_new(filter='', max_novel_id=100000000)

        return jsonify(json_result)
    except Exception as e:

        return jsonify({"error": str(e)}), 500

        # return jsonify({"message": "Hello, World!"})
        # max id = 22725727


@app.route('/search_novel', methods=['GET'])
def search_novel():
    try:
        all_novels = []
        offset = 0
        max_offset = 120000

        while offset <= max_offset:
            print(f"Fetching results with offset: {offset}")
            json_result = api.search_novel(
                word='Naruto',
                search_target='partial_match_for_tags',
                sort='date_desc',
                offset=offset
            )

            if 'novels' in json_result:
                novels = json_result['novels']
                if not novels:
                    break
                all_novels.extend(novels)
                offset += 30
            else:
                break

        high_word_count_novels = []
        processed_series_ids = set()

        for novel in all_novels:
            try:
                series_id = novel['series']['id']

                if series_id in processed_series_ids:
                    continue

                print(f"Checking series id: {series_id}")

                series_info = api.novel_series(int(series_id))

                if 'novel_series_detail' in series_info and series_info['novel_series_detail']['total_character_count'] > 100000:
                    high_word_count_novels.append(novel)
                    processed_series_ids.add(series_id)
            except KeyError as ke:
                print(f"KeyError: {ke} in novel: {novel}")
            except Exception as e:
                print(f"Exception: {e} in processing series id: {series_id}")

        return jsonify(high_word_count_novels)

    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/webview', methods=['GET'])
def webview():
    return api.webview_novel(21827107)


if __name__ == '__main__':
    app.run(debug=True)
