def diary_to_dict(diary):
    return {
        "id": diary.id,
        "Diaryuserid": diary.Diaryuserid,
        "Date": diary.Date.isoformat(),  # datetime 객체를 문자열로 변환
        "Diarycontent": diary.Diarycontent,
        "Response": diary.Response
    }
