# Notion-Tistory



- [Intro](#Intro)
- [requirements](#requirements)
- [사용법](#사용법)
- [이용범위](#이용범위)



#### Intro

노션 글을 자동으로 티스토리에 업로드해주는 파이썬 파일로 게시글 제목을 입력하면 티스토리에 자동 업로드될 수 있도록 만들었습니다.

본인은 비전공생이며 오류가 많이 발생할 수 있습니다.



#### requirements

- python
- libraries: json, requests

#### 사용법

##### 1. info.json: `#`부분에 실제값을 채워 넣는다

- 현재 경로에 `info.json` 파일 생성해야 함
- 필수입력: 티스토리 토큰, 티스토리 블로그 이름, 노션 토큰, 노션 데이터베이스 제목, 노션 데이터베이스 ID
- 파일 구조

```{json}
    {
	"tistory": {
		"URL": "https://www.tistory.com/apis/",
		"ACCESS_TOKEN": "#티스토리 토큰",
		"BLOG_NAME": "#블로그 명"
	},
	"notion": {
		"URL": "https://api.notion.com/v1/",
		"TOKEN": "#노션 토큰",
		"DATABASE": {
			"#데이터베이스 제목": {
				"id": "#데이터베이스 ID",
				"page": {}
			}
		}
	}
}
```

##### 2. 노션 데이터베이스 세부항목 설정

- `태그` 
    - 속성유형: `다중선택`
    - 값: 티스토리 블로그 태그
- `카테고리`
    - 속성유형: `선택`
    - 값: 티스토리 카테고리 이름
    - 공부 > 머신러닝 카테고리가 있을 시 '공부/머신러닝'으로 기입

##### 3. 티스토리 스킨 HTML 편집

- 인라인 수식

```{html}
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <script>
    MathJax = {
    tex: {
        inlineMath: [['$', '$'], ['\\(', '\\)']]
    }
    };
    </script>
    <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
```

- 코드블럭 하이라이트

```{html}
    <link rel="stylesheet" href="//cdn.jsdelivr.net/gh/highlightjs/cdn-release@10.7.1/build/styles/mono-blue.min.css">
    <script src="//cdn.jsdelivr.net/gh/highlightjs/cdn-release@10.7.1/build/highlight.min.js"></script>
    <script>hljs.initHighlightingOnLoad();</script>
```

##### 4. TistoryApi.py 실행

- 노션 게시글 제목을 입력(주의 ""제외하고 입력할 것!)
- 자동으로 업로드 된 것을 확인할 수 있음


#### 이용범위

- 텍스트 굵기,이텔릭,밑줄,색상
- 이미지(자동 중앙정렬)
- 콜아웃
- 코드블럭, 인라인코드
- 수식블럭, 인라인수식

