from board.models import Board
from django.utils import timezone

from .public_func import delete_img_s3

from datetime import timedelta
import boto3

from config.secret_keys import SECRET_ACCESS_KEY, ACCESS_KET_ID

import logging
import io


# AWS S3 이미지 파일 삭제 스케쥴링
def crontab_every_minute():
    client = boto3.client('s3', aws_access_key_id=ACCESS_KET_ID,
                          aws_secret_access_key=SECRET_ACCESS_KEY)
    file_name = timezone.localtime().strftime('%Y-%m-%d')
    logger = logging.getLogger()

    logging.basicConfig(filename=f'{file_name}.log',
                        format='%(asctime)s %(levelname)s %(name)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)
    log_stringio = io.StringIO()
    handler = logging.StreamHandler(log_stringio)
    logger.addHandler(handler)

    try:
        time = timezone.localtime() - timedelta(days=1)

        board_datas = Board.objects.filter(
            post_create__startswith=time.strftime('%Y-%m-%d')).only('post_content')

        content_list = list()
        for board_data in board_datas:
            content_list.append(board_data.post_content)
        delete_img_s3(content_list, bool=False)
        logging.info(f'{file_name}_success')
    except Exception as e:
        logging.info(f'{file_name}_fail_error code: {e}')

    client.upload_file(
        f'{file_name}.log',
        'poty',
        f'log/{file_name}.log'
        )
