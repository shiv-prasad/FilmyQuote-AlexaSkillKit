import json
import requests
import random

SKILL_NAME = "FILMY QUOTE"
NOT_FOUND = {
    "default": [
        "Sorry I cant find any dialogue",
        "Not able to get any dialogue for you. Sorry!",
        "Sorry, I am not able to find any dialogue for you right now"
    ],
    "tag": [
        "Sorry I cant find any {tag} dialogue",
        "Not able to get any {tag} dialogue for you. Sorry!",
        "Sorry, I am not able to find any {tag} dialogue for you right now"
    ],
    "year": [
        "Sorry I cant find any {year}s dialogue by",
        "Not able to get any dialogue in {year} for you. Sorry!",
        "Sorry, I am not able to find any {year}s dialogue for you right now"
    ],
    "year_tag": [
        "Sorry I cant find any {tag} dialogue in {year}",
        "Not able to get any {tag} dialogue in {year} for you. Sorry!",
        "Sorry, I am not able to find any {tag} dialogue told in {year} for you right now"
    ],
    "movie": [
        "Sorry I cant find any dialogue from {movie}",
        "Not able to get any dialogue from {movie} for you. Sorry!",
        "Sorry, I am not able to find any {movie}'s dialogue for you right now"
    ],
    "star": [
        "Sorry I cant find any dialogue by {star}",
        "Not able to get any dialogue by {star} for you. Sorry!",
        "Sorry, I am not able to find any {star}'s dialogue for you right now"
    ]
}
FOUND = {
    "default": [
        "Here's your dialogue by {dialogue_star} in {dialogue_movie}: {dialogue}",
        "Here's a dialogue for you by {dialogue_star} in {dialogue_movie}: {dialogue}"
    ],
    "tag": [
        "Here's your {tag} dialogue by {dialogue_star} in {dialogue_movie}: {dialogue}",
        "Here's a {tag} dialogue for you by {dialogue_star} in {dialogue_movie}: {dialogue}"
    ],
    "year": [
        "Here's your dialogue from the year {year} by {dialogue_star} in {dialogue_movie}: {dialogue}",
        "Here's a dialogue for you from the year {year} by {dialogue_star} in {dialogue_movie}: {dialogue}"
    ],
    "year_tag": [
        "Here's your {tag} dialogue from the year {year} by {dialogue_star} in {dialogue_movie}: {dialogue}",
        "Here's a {tag} dialogue for you from the year {year} by {dialogue_star} in {dialogue_movie}: {dialogue}"
    ],
    "movie": [
        "Here's your dialogue from the movie {movie} by {dialogue_star}: {dialogue}",
        "Here's a dialogue for you from the movie {movie} by {dialogue_star}: {dialogue}"
    ],
    "star": [
        "Here's your dialogue by {star} in {dialogue_movie}: {dialogue}",
        "Here's a dialogue for you by {star} in {dialogue_movie}: {dialogue}"
    ]
}

def build_Card(card_type, title, dialogue, poster):
    card = {}
    card['type'] = card_type
    card['title'] = title
    card['content'] = dialogue
    return card

def build_PlainSpeech(output_speech):
    speech = {}
    speech['type'] = 'PlainText'
    speech['text'] = output_speech
    return speech

def statement(output_speech="", card_type=None, title=None, dialogue=None, poster=None):
    speechlet = {}
    speechlet['outputSpeech'] = build_PlainSpeech(output_speech)
    if card_type:
        speechlet['card'] = build_Card(card_type, title, dialogue, poster)
    speechlet['shouldEndSession'] = True
    return build_response(speechlet)

def build_response(message):
    response = {}
    response['version'] = '1.0'
    response['response'] = message
    return response

def get_movie_search_result(search_query):
    try:
        url = "https://www.filmyquote.tk/api/search-movies-star/?query={query}".format(query=search_query)
        resp = requests.get(url)
        if resp.status_code == 200:
            results = json.loads(resp.content)['results']
            relevant = []
            for each_result in results:
                if each_result['type'] == 'movie':
                    relevant.append(each_result['value'])
            if len(relevant) > 0:
                final_result = random.choice(relevant)
                final_result_parts = final_result.split('|')
                return final_result_parts[0], final_result_parts[1]
            else:
                return None, None
        else:
            return None, None
    except Exception as e:
        print str(e)
        return None, None

def get_tag_id(tag_query):
    try:
        url = "https://www.filmyquote.tk/api/get-tags/"
        resp = requests.get(url)
        if resp.status_code == 200:
            tags = json.loads(resp.content)['tags']
            for each_tag in tags:
                if each_tag['name'].strip().lower() == tag_query.strip().lower():
                    return each_tag['id']
            return None
        else:
            return None
    except Exception as e:
        print str(e)
        return None

def get_dialog(tags='0', min_year='1990',  max_year='2018', name='0', year='0', star='0'):
    try:
        url = "https://www.filmyquote.tk/api/get-dialogues/?include_tags={tags}&year_min={min_year}&year_max={max_year}&movie_name={name}&movie_year={year}&star={star}".format(tags=tags, min_year=min_year, max_year=max_year, name=name, year=year, star=star)
        resp = requests.get(url)
        if resp.status_code == 200:
            data = json.loads(resp.content)['dialogue']
            if data['star'] in ["", "unknown"]:
                data['star'] = "Anonymous"
            if data['star_image_url'].strip() == "":
                data['star_image_url'] = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxNTAiIGhlaWdodD0iMTUwIiB2aWV3Qm94PSIwIDAgMTUwIDE1MCI+CiAgPGcgZmlsbD0ibm9uZSIgZmlsbC1ydWxlPSJldmVub2RkIj4KICAgIDxyZWN0IHdpZHRoPSIxNTAiIGhlaWdodD0iMTUwIiBmaWxsPSIjRkZGIiBvcGFjaXR5PSIuMDQyIi8+CiAgICA8ZyBmaWxsPSIjM0U1MzY0IiBmaWxsLXJ1bGU9Im5vbnplcm8iIG9wYWNpdHk9Ii43NDQiIHRyYW5zZm9ybT0idHJhbnNsYXRlKDM4LjUxNCA0MC41NCkiPgogICAgICA8ZWxsaXBzZSBjeD0iNDguNzgyIiBjeT0iMzEuOTgxIiByeD0iNi4yMDgiIHJ5PSI2LjM4NyIvPgogICAgICA8ZWxsaXBzZSBjeD0iMjQuNjYiIGN5PSIzMS45ODEiIHJ4PSI2LjIwNiIgcnk9IjYuMzg3Ii8+CiAgICAgIDxwYXRoIGQ9Ik0zNy4wMjU2NzU3LDU3LjU2NjU1NDEgQzQzLjE5Nzk3Myw1Ny41NjY1NTQxIDQ3LjE5NDI1NjgsNTIuNjAyMzY0OSA0NS41MTU4Nzg0LDQ5LjcyODA0MDUgQzQzLjQ2NTU0MDUsNTAuOTUwMzM3OCA0MC40MjI5NzMsNTEuNzI1Njc1NyAzNy4wMjU2NzU3LDUxLjcyNTY3NTcgQzMzLjYyODM3ODQsNTEuNzI1Njc1NyAzMC41ODU4MTA4LDUwLjk1MDMzNzggMjguNTM1NDczLDQ5LjcyODA0MDUgQzI2Ljg1NzA5NDYsNTIuNjAxMzUxNCAzMC44NTMzNzg0LDU3LjU2NjU1NDEgMzcuMDI1Njc1Nyw1Ny41NjY1NTQxIFoiLz4KICAgICAgPHBhdGggZD0iTTM2LjcyMDYwODEsMC4wMzU0NzI5NzMgQzE2Ljg4MDA2NzYsMC4wMzU0NzI5NzMgMC43Mzc4Mzc4MzgsMTYuMTc2Njg5MiAwLjczNzgzNzgzOCwzNi4wMTYyMTYyIEMwLjczNzgzNzgzOCw1NS44NTU3NDMyIDE2Ljg4MDA2NzYsNzEuOTk3OTczIDM2LjcyMDYwODEsNzEuOTk3OTczIEM1Ni41NjAxMzUxLDcxLjk5Nzk3MyA3Mi43MDEzNTE0LDU1Ljg1NTc0MzIgNzIuNzAxMzUxNCwzNi4wMTYyMTYyIEM3Mi43MDEzNTE0LDE2LjE3NTY3NTcgNTYuNTYxMTQ4NiwwLjAzNTQ3Mjk3MyAzNi43MjA2MDgxLDAuMDM1NDcyOTczIFogTTM2LjcyMDYwODEsNjYuMjUxMzUxNCBDMjEuNjc1LDY2LjI1MTM1MTQgOS4xNjUyMDI3LDU1LjIwNTA2NzYgNi44NjY1NTQwNSw0MC43OTc5NzMgQzYuOTQzNTgxMDgsMjEuNDU3MDk0NiAyMy43Mzg1MTM1LDMyLjA4NTgxMDggMjMuNzM4NTEzNSwxMC45NjMxNzU3IEMyNC41MDg3ODM4LDIxLjcwODQ0NTkgMzMuMTczMzEwOCwzOS4yNTAzMzc4IDY2LjU3NjY4OTIsMzEuMjU3NzcwMyBDNjYuODIyOTczLDMyLjgwODQ0NTkgNjYuOTU0NzI5NywzNC4zOTc2MzUxIDY2Ljk1NDcyOTcsMzYuMDE2MjE2MiBDNjYuOTU0NzI5Nyw1Mi42ODc1IDUzLjM5MjkwNTQsNjYuMjUxMzUxNCAzNi43MjA2MDgxLDY2LjI1MTM1MTQgWiIvPgogICAgPC9nPgogIDwvZz4KPC9zdmc+Cg=="
            else:
                data['star_image_url'] = "https://image.tmdb.org/t/p/w500_and_h500_face/{url}".format(url=data['star_image_url'])
            return {
                "dialogue": data['dialogue'],
                "star": data['star'],
                "movie": data['movie_name'],
                "poster": data['star_image_url']
            }
        else:
            return None
    except Exception as e:
        print str(e)
        return None

def getDialogIntentHandler():
    dialog = get_dialog()
    if dialog:
        output_dialog = random.choice(FOUND['default']).format(dialogue=dialog['dialogue'], dialogue_star=dialog['star'], dialogue_movie=dialog['movie'])
        title = "{star} ({movie})".format(star=dialog['star'], movie=dialog['movie'])
        return statement(output_speech=output_dialog, card_type='Simple', title=title, dialogue=dialog['dialogue'], poster=dialog['poster'])
    else:
        output_speech = random.choice(NOT_FOUND['default'])
        return statement(output_speech=output_dialog)

def getDialogWithTagHandler(slots):
    tag = slots.get('tag')
    dialog = None
    if tag:
        tag_value = tag.get('value')
        if tag_value:
            tag_id = get_tag_id(tag_value)
            if tag_id:
                dialog = get_dialog(tags=tag_id)
                if dialog:
                    output_dialog = random.choice(FOUND['tag']).format(tag=tag_value, dialogue=dialog['dialogue'], dialogue_star=dialog['star'], dialogue_movie=dialog['movie'])
                    title = "{star} ({movie})".format(star=dialog['star'], movie=dialog['movie'])
                    return statement(output_speech=output_dialog, card_type='Simple', title=title, dialogue=dialog['dialogue'], poster=dialog['poster'])
                else:
                    output_dialog = random.choice(NOT_FOUND['tag']).format(tag=tag_value)
                    return statement(output_speech=output_dialog)
            else:
                output_dialog = random.choice(NOT_FOUND['tag']).format(tag=tag_value)
                return statement(output_speech=output_dialog)
        else:
            output_dialog = random.choice(NOT_FOUND['default'])
            return statement(output_speech=output_dialog)
    else:
        output_dialog = random.choice(NOT_FOUND['default'])
        return statement(output_speech=output_dialog)

def getDialogWithYearHandler(slots):
    year = slots.get('year')
    dialog = None
    if year:
        year_value = year.get('value')
        if year_value:
            dialog = get_dialog(min_year=year_value, max_year=year_value)
            if dialog:
                output_dialog = random.choice(FOUND['year']).format(year=year_value, dialogue=dialog['dialogue'], dialogue_star=dialog['star'], dialogue_movie=dialog['movie'])
                title = "{star} ({movie})".format(star=dialog['star'], movie=dialog['movie'])
                return statement(output_speech=output_dialog, card_type='Simple', title=title, dialogue=dialog['dialogue'], poster=dialog['poster'])
            else:
                output_dialog = random.choice(NOT_FOUND['year']).format(year=year_value)
                return statement(output_speech=output_dialog)
        else:
            output_dialog = random.choice(NOT_FOUND['default'])
            return statement(output_speech=output_dialog)
    else:
        output_dialog = random.choice(NOT_FOUND['default'])
        return statement(output_speech=output_dialog)

def getDialogWithTagAndYearHandler(slots):
    tag = slots.get('tag')
    year = slots.get('year')
    dialog = None
    if tag and year:
        tag_value = tag.get('value')
        year_value = year.get('value')
        tag_id = None
        if tag_value:
            tag_id = get_tag_id(tag_value)
        if tag_id and year_value:
            dialog = get_dialog(tags=tag_id, min_year=year_value, max_year=year_value)
            if dialog:
                output_dialog = random.choice(FOUND['year_tag']).format(tag=tag_value, year=year_value, dialogue=dialog['dialogue'], dialogue_star=dialog['star'], dialogue_movie=dialog['movie'])
                title = "{star} ({movie})".format(star=dialog['star'], movie=dialog['movie'])
                return statement(output_speech=output_dialog, card_type='Simple', title=title, dialogue=dialog['dialogue'], poster=dialog['poster'])
            else:
                output_dialog = random.choice(NOT_FOUND['year_tag']).format(tag=tag_value, year=year_value)
                return statement(output_speech=output_dialog)
        else:
            output_dialog = random.choice(NOT_FOUND['default'])
            return statement(output_speech=output_dialog)
    else:
        output_dialog = random.choice(NOT_FOUND['default'])
        return statement(output_speech=output_dialog)

def getDialogWithMovieHandler(slots):
    movie = slots.get('movie')
    dialog = None
    if movie:
        movie_value = movie.get('value')
        if movie_value:
            movie_filter, year_filter = get_movie_search_result(movie_value)
            if movie_filter:
                dialog = get_dialog(name=movie_filter, year=year_filter)
                if dialog:
                    output_dialog = random.choice(FOUND['movie']).format(movie=movie_value, dialogue=dialog['dialogue'], dialogue_star=dialog['star'])
                    title = "{star} ({movie})".format(star=dialog['star'], movie=dialog['movie'])
                    return statement(output_speech=output_dialog, card_type='Simple', title=title, dialogue=dialog['dialogue'], poster=dialog['poster'])
                else:
                    output_dialog = random.choice(NOT_FOUND['movie']).format(movie=movie_value)
                    return statement(output_speech=output_dialog)
            else:
                output_dialog = random.choice(NOT_FOUND['movie']).format(movie=movie_value)
                return statement(output_speech=output_dialog)
        else:
            output_dialog = random.choice(NOT_FOUND['default'])
            return statement(output_speech=output_dialog)
    else:
        output_dialog = random.choice(NOT_FOUND['default'])
        return statement(output_speech=output_dialog)

def getDialogWithActorHandler(slots):
    star = slots.get('actor')
    dialog = None
    if star:
        star_value = star.get('value')
        if star_value:
            dialog = get_dialog(star=star_value)
            if dialog:
                output_dialog = random.choice(FOUND['star']).format(star=star_value, dialogue=dialog['dialogue'], dialogue_movie=dialog['movie'])
                title = "{star} ({movie})".format(star=dialog['star'], movie=dialog['movie'])
                return statement(output_speech=output_dialog, card_type='Simple', title=title, dialogue=dialog['dialogue'], poster=dialog['poster'])
            else:
                output_dialog = random.choice(NOT_FOUND['star']).format(star=star_value)
                return statement(output_speech=output_dialog)
        else:
            output_dialog = random.choice(NOT_FOUND['default'])
            return statement(output_speech=output_dialog)
    else:
        output_dialog = random.choice(NOT_FOUND['default'])
        return statement(output_speech=output_dialog)

def lambda_handler(event, context):
    request_type = event['request']['type']
    if request_type == 'IntentRequest':
        intent = event['request']['intent']['name']
        if intent:
            if intent == 'GetDialogIntent':
                return getDialogIntentHandler()
            elif intent == 'GetDialogWithTag':
                slots = event['request']['intent'].get('slots', {})
                return getDialogWithTagHandler(slots)
            elif intent == 'GetDialogWithYear':
                slots = event['request']['intent'].get('slots', {})
                return getDialogWithYearHandler(slots)
            elif intent == 'GetDialogWithTagAndYear':
                slots = event['request']['intent'].get('slots', {})
                return getDialogWithTagAndYearHandler(slots)
            elif intent == 'GetDialogWithMovie':
                slots = event['request']['intent'].get('slots', {})
                return getDialogWithMovieHandler(slots)
            elif intent == 'GetDialogWithActor':
                slots = event['request']['intent'].get('slots', {})
                return getDialogWithActorHandler(slots)
            else:
                return getDialogIntentHandler()
        else:
            return getDialogIntentHandler()
    else:
        return getDialogIntentHandler()
