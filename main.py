from pprint import pprint
import time
import vk_api

# авторизовать приложение из https://vkhost.github.io/ и записать айди приложения в переменную APP_ID

APP_ID = 5776857
LOGIN = 'login'
PASSWORD = 'password'
NAME = 'Название'
DESCRIPTION = 'Подписывайтесь на нас!'


def authenticate(login, password):
    print('Авторизуюсь...')
    vk_session = vk_api.VkApi(app_id=APP_ID, login=login, password=password)
    vk_session.auth()
    vk = vk_session.get_api()
    return vk


def get_groups(vk, user_id):
    groups = vk.groups.get(user_id=user_id, extended=1)
    return [group['id'] for group in groups['items']]


def get_clips(vk, user_id, group_id):
    print('Собираю видео...')
    videos = []
    offset = 0
    count = 200

    while True:
        response = vk.video.get(
            owner_id=-group_id, album_id=-6, offset=offset, count=count
        )
        # response = vk.wall.get(
        #     owner_id=-group_id, filter='video', offset=offset, count=count
        # )
        items = response['items']
        if not items:
            break

        for video in items:
            # if video.get('created_by') == user_id:
            #     continue
            if video.get('description') != DESCRIPTION:
                videos.append(video)

        offset += count
        time.sleep(10)
    print(f'Собирано видео: {len(videos)} шт.')
    return videos


def rename_clips(vk, clips, group_id, name, desc):
    for clip in clips:
        vk.video.edit(
            owner_id=-group_id,
            video_id=clip['id'],
            desc=desc,  # name=name
        )
        # vk.video.edit(
        #     owner_id=-group_id,
        #     video_id=clip.get('attachments')[0].get('video').get('id'),
        #     desc=desc,  # name=name
        # )
        res = f'У клипа {clip["id"]} "{clip["title"]}" было изменено описание'
        print(res)
        time.sleep(15)


def main():
    vk = authenticate(LOGIN, PASSWORD)
    user_id = vk.users.get()[0]['id']
    print(user_id)
    groups = get_groups(vk, user_id)

    for group_id in groups:
        print(group_id)
        clips = get_clips(vk, user_id, group_id)
        pprint(clips[0])
        rename_clips(vk, clips, group_id, NAME, DESCRIPTION)


if __name__ == '__main__':
    main()
