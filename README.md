### youtube 좋아요 한 영상 crawling으로 다운받기

첫번쨰
selenium을 통해 자동화 하는건 google이 막고 있기 때문에 google에서 직접적으로 로그인 하지는 못하고, stackoverflow 사이트로 우회해서 로그인 진행함
간접 로그인을 하고, youtube playlist로 redirect함

두번째
selenium을 통해 구글 로그인 하는것에 대해 강화가 더 심해져서 selenium stealth 기능을 추가함

2021-06-11 세번째 업데이트
stackoverflow로 로그인하면 captcha에 걸림 네이버 captcha 우회는 찾아지지만 구글은 아직 해결책이 없는걸로 확인함
앞에서 stealth 기능을 추가 했더니 youtube로 바로 로그인이 가능해져서 시작 경로만 수정
