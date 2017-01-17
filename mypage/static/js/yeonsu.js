;(function(){/**
 * Add, remove, modify field in URL query string.
 * https://github.com/hyeonseok/QueryString
 */
var QueryString = {
	parseUrl: function (href) {
		return {
			'path': href.split('#')[0].split('?')[0],
			'query': href.indexOf('?') > -1 ? href.split('?')[1].split('#')[0] : '',
			'hash': href.split('#')[1] || ''
		}
	},

	makeUrl: function (parsed) {
		return parsed.path + (parsed.query.length > 0 ? '?' + parsed.query : '') + (parsed.hash.length > 0 ? '#' + parsed.hash : '');
	},

	getParameter: function (href, parameter) {
		var parsed = this.parseUrl(href),
			splited,
			value = [],
			i;

		for (i = 0, splited = parsed.query.split('&'); i < splited.length; i++) {
			if (splited[i].indexOf(parameter + '=') > -1 || splited[i].indexOf(encodeURIComponent(parameter) + '=') > -1) {
				value.push(splited[i].split('=')[1]);
			}
		}

		return value.length === 0 ? undefined : (value.length === 1 ? value[0] : value);
	},

	addParameter: function (href, parameter, value) {
		var parsed = this.parseUrl(href),
			query = [],
			i;

		if (parsed.query.indexOf(parameter + '=') > -1) {
			for (i = 0, splited = parsed.query.split('&'); i < splited.length; i++) {
				if (splited[i].indexOf(parameter + '=') === -1 && splited[i].indexOf(encodeURIComponent(parameter) + '=') === -1) {
					query.push(splited[i]);
				}
			}
		} else if (parsed.query.length > 0) {
			query.push(parsed.query);
		}
		query.push(parameter + '=' + value);

		parsed.query = query.join('&');

		return this.makeUrl(parsed);
	},

	removeParameter: function (href, parameter) {
		var parsed = this.parseUrl(href),
			query = [],
			i;

		for (i = 0, splited = parsed.query.split('&'); i < splited.length; i++) {
			if (splited[i].indexOf(parameter + '=') > -1 || splited[i].indexOf(encodeURIComponent(parameter) + '=') > -1) {
				continue;
			}

			if (splited[i].length > 0) {
				query.push(splited[i]);
			}
		}

		parsed.query = query.join('&');

		return this.makeUrl(parsed);
	},

	addQueryString: function (href, queryString) {
		var parsed = this.parseUrl(href);

		parsed.query += parsed.query.length > 0 && queryString.length > 0 ? '&' + queryString : '';

		return this.makeUrl(parsed);
	}
};
function QuizMonkey() {}

QuizMonkey.prototype = {
	quizType: null,
	createType: null,
	$el: null,
	$question: null,
	$result: null,
	$counter: null,
	$window: null,
	$goResultButton: null,
	quizId: null,
	distId: null,

	loadingAnimation: {
		el: null,
		animationSequence: [1, 2, 3, 4, 5, 6, 7, 6, 5, 4, 3, 2, 1, 8, 9, 10, 11, 12, 12, 11, 10, 9, 8, 1, 13, 14, 15, 16, 17, 18, 19, 18, 17, 16, 15, 14, 13],
		loading: null,

		init: function (element) {
			this.el = element;
		},

		showLoading: function () {
			var animationSequence = this.animationSequence;
			var currentSequence = 0;
			var el = this.el;
			this.loading = window.setInterval(function () {
				if (currentSequence == animationSequence.length - 1) {
					currentSequence = 0;
				}
				el.style.backgroundPosition = '-' + (animationSequence[currentSequence++] - 1) * 100 + 'px 0';
			}, 90);
		},

		hideLoading: function () {
			window.clearInterval(this.loading);
		},
	},

	init: function (quizType) {
var html = '<strong class="tit_quiz">연애유형 테스트</strong><div class="quiz-monkey-question quiztype-0"><ul class="list_quiz"><li><div class="intro_quiz" data-pick="parsed-quiz-intro-text"><p>본 연애심리검사는 필립 셰이버 교수가 고안한 [연애유형 검사]를 한국인의 연애에 알맞게 변형시킨 것입니다. 내 연애스타일의 특성과 문제점에 대한 모든 궁금증이 풀릴 거예요!</p></div><p class="counter"><span>1</span>명이 참여하였습니다.</p><button class="btn_quiz intro">시작하기</button></li><li class="quiz-monkey-question-0"><p class="progress_quiz"><span class="active on">1</span><span>2</span><span>3</span><span>4</span><span>5</span><span>6</span><span>7</span><span>8</span><span>9</span><span>10</span><span>11</span><span>12</span><span>13</span><span>14</span><span>15</span></p><div class="question_header"><div class="question_quiz question_thumb question_thumb2" data-pick="parsed-questions-0-question"><span class="wrap_thumb"><img src="http://t1.daumcdn.net/liveboard/issue/585a487189a14a7a85b631ae51cf190c.png" alt="" /></span></div></div><div class="answer_list"><ul class="list_answer "><li><div class="answer_btn"><button class="button" data-weight="1,1,1,1,1" data-pick="parsed-questions-0-answer-0-text" data-pick-selector="p"><p>매우 그렇다</p></button></div></li><li><div class="answer_btn"><button class="button" data-weight="1,1,1,1" data-pick="parsed-questions-0-answer-1-text" data-pick-selector="p"><p>그렇다</p></button></div></li><li><div class="answer_btn"><button class="button" data-weight="1,1,1" data-pick="parsed-questions-0-answer-2-text" data-pick-selector="p"><p>보통이다</p></button></div></li><li><div class="answer_btn"><button class="button" data-weight="1,1" data-pick="parsed-questions-0-answer-3-text" data-pick-selector="p"><p>그렇지 않다</p></button></div></li><li><div class="answer_btn"><button class="button" data-weight="1" data-pick="parsed-questions-0-answer-4-text" data-pick-selector="p"><p>전혀 그렇지 않다</p></button></div></li></ul></div></li><li class="quiz-monkey-question-1"><p class="progress_quiz"><span class="active">1</span><span class="active on">2</span><span>3</span><span>4</span><span>5</span><span>6</span><span>7</span><span>8</span><span>9</span><span>10</span><span>11</span><span>12</span><span>13</span><span>14</span><span>15</span></p><div class="question_header"><div class="question_quiz question_thumb question_thumb2" data-pick="parsed-questions-1-question"><span class="wrap_thumb"><img src="http://t1.daumcdn.net/liveboard/issue/db4cb0ec8e13415896155cff3224d627.png" alt="" /></span></div></div><div class="answer_list"><ul class="list_answer "><li><div class="answer_btn"><button class="button" data-weight="0,0,0,0,0" data-pick="parsed-questions-1-answer-0-text" data-pick-selector="p"><p>매우 그렇다</p></button></div></li><li><div class="answer_btn"><button class="button" data-weight="0,0,0,0" data-pick="parsed-questions-1-answer-1-text" data-pick-selector="p"><p>그렇다</p></button></div></li><li><div class="answer_btn"><button class="button" data-weight="0,0,0" data-pick="parsed-questions-1-answer-2-text" data-pick-selector="p"><p>보통이다</p></button></div></li><li><div class="answer_btn"><button class="button" data-weight="0,0" data-pick="parsed-questions-1-answer-3-text" data-pick-selector="p"><p>그렇지 않다</p></button></div></li><li><div class="answer_btn"><button class="button" data-weight="0" data-pick="parsed-questions-1-answer-4-text" data-pick-selector="p"><p>전혀 그렇지 않다</p></button></div></li></ul></div></li><li class="quiz-monkey-question-2"><p class="progress_quiz"><span class="active">1</span><span class="active">2</span><span class="active on">3</span><span>4</span><span>5</span><span>6</span><span>7</span><span>8</span><span>9</span><span>10</span><span>11</span><span>12</span><span>13</span><span>14</span><span>15</span></p><div class="question_header"><div class="question_quiz question_thumb question_thumb2" data-pick="parsed-questions-2-question"><span class="wrap_thumb"><img src="http://t1.daumcdn.net/liveboard/issue/72bb05c42c934f4397c5037485c554e9.png" alt="" /></span></div></div><div class="answer_list"><ul class="list_answer "><li><div class="answer_btn"><button class="button" data-weight="2,2,2,2,2" data-pick="parsed-questions-2-answer-0-text" data-pick-selector="p"><p>매우 그렇다</p></button></div></li><li><div class="answer_btn"><button class="button" data-weight="2,2,2,2" data-pick="parsed-questions-2-answer-1-text" data-pick-selector="p"><p>그렇다</p></button></div></li><li><div class="answer_btn"><button class="button" data-weight="2,2,2" data-pick="parsed-questions-2-answer-2-text" data-pick-selector="p"><p>보통이다</p></button></div></li><li><div class="answer_btn"><button class="button" data-weight="2,2" data-pick="parsed-questions-2-answer-3-text" data-pick-selector="p"><p>그렇지 않다</p></button></div></li><li><div class="answer_btn"><button class="button" data-weight="2" data-pick="parsed-questions-2-answer-4-text" data-pick-selector="p"><p>전혀 그렇지 않다</p></button></div></li></ul></div></li><li class="quiz-monkey-question-3"><p class="progress_quiz"><span class="active">1</span><span class="active">2</span><span class="active">3</span><span class="active on">4</span><span>5</span><span>6</span><span>7</span><span>8</span><span>9</span><span>10</span><span>11</span><span>12</span><span>13</span><span>14</span><span>15</span></p><div class="question_header"><div class="question_quiz question_thumb question_thumb2" data-pick="parsed-questions-3-question"><span class="wrap_thumb"><img src="http://t1.daumcdn.net/liveboard/issue/e47947d3ee7541b3b9462e62d1559c18.png" alt="" /></span></div></div><div class="answer_list"><ul class="list_answer "><li><div class="answer_btn"><button class="button" data-weight="1,1,1,1,1" data-pick="parsed-questions-3-answer-0-text" data-pick-selector="p"><p>매우 그렇다</p></button></div></li><li><div class="answer_btn"><button class="button" data-weight="1,1,1,1" data-pick="parsed-questions-3-answer-1-text" data-pick-selector="p"><p>그렇다</p></button></div></li><li><div class="answer_btn"><button class="button" data-weight="1,1,1" data-pick="parsed-questions-3-answer-2-text" data-pick-selector="p"><p>보통이다</p></button></div></li><li><div class="answer_btn"><button class="button" data-weight="1,1" data-pick="parsed-questions-3-answer-3-text" data-pick-selector="p"><p>그렇지 않다</p></button></div></li><li><div class="answer_btn"><button class="button" data-weight="1" data-pick="parsed-questions-3-answer-4-text" data-pick-selector="p"><p>전혀 그렇지 않다</p></button></div></li></ul></div></li><li class="quiz-monkey-question-4"><p class="progress_quiz"><span class="active">1</span><span class="active">2</span><span class="active">3</span><span class="active">4</span><span class="active on">5</span><span>6</span><span>7</span><span>8</span><span>9</span><span>10</span><span>11</span><span>12</span><span>13</span><span>14</span><span>15</span></p><div class="question_header"><div class="question_quiz question_thumb question_thumb2" data-pick="parsed-questions-4-question"><span class="wrap_thumb"><img src="http://t1.daumcdn.net/liveboard/issue/f3c738731f12448c819225113b39e72b.png" alt="" /></span></div></div><div class="answer_list"><ul class="list_answer "><li><div class="answer_btn"><button class="button" data-weight="0,0,0,0,0" data-pick="parsed-questions-4-answer-0-text" data-pick-selector="p"><p>매우 그렇다</p></button></div></li><li><div class="answer_btn"><button class="button" data-weight="0,0,0,0" data-pick="parsed-questions-4-answer-1-text" data-pick-selector="p"><p>그렇다</p></button></div></li><li><div class="answer_btn"><button class="button" data-weight="0,0,0" data-pick="parsed-questions-4-answer-2-text" data-pick-selector="p"><p>보통이다</p></button></div></li><li><div class="answer_btn"><button class="button" data-weight="0,0" data-pick="parsed-questions-4-answer-3-text" data-pick-selector="p"><p>그렇지 않다</p></button></div></li><li><div class="answer_btn"><button class="button" data-weight="0" data-pick="parsed-questions-4-answer-4-text" data-pick-selector="p"><p>전혀 그렇지 않다</p></button></div></li></ul></div></li><li class="quiz-monkey-question-5"><p class="progress_quiz"><span class="active">1</span><span class="active">2</span><span class="active">3</span><span class="active">4</span><span class="active">5</span><span class="active on">6</span><span>7</span><span>8</span><span>9</span><span>10</span><span>11</span><span>12</span><span>13</span><span>14</span><span>15</span></p><div class="question_header"><div class="question_quiz question_thumb question_thumb2" data-pick="parsed-questions-5-question"><span class="wrap_thumb"><img src="http://t1.daumcdn.net/liveboard/issue/38a6d11322e7463a921be013b81e450e.png" alt="" /></span></div></div><div class="answer_list"><ul class="list_answer "><li><div class="answer_btn"><button class="button" data-weight="2,2,2,2,2" data-pick="parsed-questions-5-answer-0-text" data-pick-selector="p"><p>매우 그렇다</p></button></div></li><li><div class="answer_btn"><button class="button" data-weight="2,2,2,2" data-pick="parsed-questions-5-answer-1-text" data-pick-selector="p"><p>그렇다</p></button></div></li><li><div class="answer_btn"><button class="button" data-weight="2,2,2" data-pick="parsed-questions-5-answer-2-text" data-pick-selector="p"><p>보통이다</p></button></div></li><li><div class="answer_btn"><button class="button" data-weight="2,2" data-pick="parsed-questions-5-answer-3-text" data-pick-selector="p"><p>그렇지 않다</p></button></div></li><li><div class="answer_btn"><button class="button" data-weight="2" data-pick="parsed-questions-5-answer-4-text" data-pick-selector="p"><p>전혀 그렇지 않다</p></button></div></li></ul></div></li><li class="quiz-monkey-question-6"><p class="progress_quiz"><span class="active">1</span><span class="active">2</span><span class="active">3</span><span class="active">4</span><span class="active">5</span><span class="active">6</span><span class="active on">7</span><span>8</span><span>9</span><span>10</span><span>11</span><span>12</span><span>13</span><span>14</span><span>15</span></p><div class="question_header"><div class="question_quiz question_thumb question_thumb2" data-pick="parsed-questions-6-question"><span class="wrap_thumb"><img src="http://t1.daumcdn.net/liveboard/issue/8210d851b2424fc7913c586b793d6c86.png" alt="" /></span></div></div><div class="answer_list"><ul class="list_answer "><li><div class="answer_btn"><button class="button" data-weight="1,1,1,1,1" data-pick="parsed-questions-6-answer-0-text" data-pick-selector="p"><p>매우 그렇다</p></button></div></li><li><div class="answer_btn"><button class="button" data-weight="1,1,1,1" data-pick="parsed-questions-6-answer-1-text" data-pick-selector="p"><p>그렇다</p></button></div></li><li><div class="answer_btn"><button class="button" data-weight="1,1,1" data-pick="parsed-questions-6-answer-2-text" data-pick-selector="p"><p>보통이다</p></button></div></li><li><div class="answer_btn"><button class="button" data-weight="1,1" data-pick="parsed-questions-6-answer-3-text" data-pick-selector="p"><p>그렇지 않다</p></button></div></li><li><div class="answer_btn"><button class="button" data-weight="1" data-pick="parsed-questions-6-answer-4-text" data-pick-selector="p"><p>전혀 그렇지 않다</p></button></div></li></ul></div></li><li class="quiz-monkey-question-7"><p class="progress_quiz"><span class="active">1</span><span class="active">2</span><span class="active">3</span><span class="active">4</span><span class="active">5</span><span class="active">6</span><span class="active">7</span><span class="active on">8</span><span>9</span><span>10</span><span>11</span><span>12</span><span>13</span><span>14</span><span>15</span></p><div class="question_header"><div class="question_quiz question_thumb question_thumb2" data-pick="parsed-questions-7-question"><span class="wrap_thumb"><img src="http://t1.daumcdn.net/liveboard/issue/6c3e91fa0d864cca88d749b1914a0947.png" alt="" /></span></div></div><div class="answer_list"><ul class="list_answer "><li><div class="answer_btn"><button class="button" data-weight="0,0,0,0,0" data-pick="parsed-questions-7-answer-0-text" data-pick-selector="p"><p>매우 그렇다</p></button></div></li><li><div class="answer_btn"><button class="button" data-weight="0,0,0,0" data-pick="parsed-questions-7-answer-1-text" data-pick-selector="p"><p>그렇다</p></button></div></li><li><div class="answer_btn"><button class="button" data-weight="0,0,0" data-pick="parsed-questions-7-answer-2-text" data-pick-selector="p"><p>보통이다</p></button></div></li><li><div class="answer_btn"><button class="button" data-weight="0,0" data-pick="parsed-questions-7-answer-3-text" data-pick-selector="p"><p>그렇지 않다</p></button></div></li><li><div class="answer_btn"><button class="button" data-weight="0" data-pick="parsed-questions-7-answer-4-text" data-pick-selector="p"><p>전혀 그렇지 않다</p></button></div></li></ul></div></li><li class="quiz-monkey-question-8"><p class="progress_quiz"><span class="active">1</span><span class="active">2</span><span class="active">3</span><span class="active">4</span><span class="active">5</span><span class="active">6</span><span class="active">7</span><span class="active">8</span><span class="active on">9</span><span>10</span><span>11</span><span>12</span><span>13</span><span>14</span><span>15</span></p><div class="question_header"><div class="question_quiz question_thumb question_thumb2" data-pick="parsed-questions-8-question"><span class="wrap_thumb"><img src="http://t1.daumcdn.net/liveboard/issue/094bb6cffe9b4e80bcf3f0d54cc14bef.png" alt="" /></span></div></div><div class="answer_list"><ul class="list_answer "><li><div class="answer_btn"><button class="button" data-weight="2,2,2,2,2" data-pick="parsed-questions-8-answer-0-text" data-pick-selector="p"><p>매우 그렇다</p></button></div></li><li><div class="answer_btn"><button class="button" data-weight="2,2,2,2" data-pick="parsed-questions-8-answer-1-text" data-pick-selector="p"><p>그렇다</p></button></div></li><li><div class="answer_btn"><button class="button" data-weight="2,2,2" data-pick="parsed-questions-8-answer-2-text" data-pick-selector="p"><p>보통이다</p></button></div></li><li><div class="answer_btn"><button class="button" data-weight="2,2" data-pick="parsed-questions-8-answer-3-text" data-pick-selector="p"><p>그렇지 않다</p></button></div></li><li><div class="answer_btn"><button class="button" data-weight="2" data-pick="parsed-questions-8-answer-4-text" data-pick-selector="p"><p>전혀 그렇지 않다</p></button></div></li></ul></div></li><li class="quiz-monkey-question-9"><p class="progress_quiz"><span class="active">1</span><span class="active">2</span><span class="active">3</span><span class="active">4</span><span class="active">5</span><span class="active">6</span><span class="active">7</span><span class="active">8</span><span class="active">9</span><span class="active on">10</span><span>11</span><span>12</span><span>13</span><span>14</span><span>15</span></p><div class="question_header"><div class="question_quiz question_thumb question_thumb2" data-pick="parsed-questions-9-question"><span class="wrap_thumb"><img src="http://t1.daumcdn.net/liveboard/issue/d36685576fed4cd4a33162dd3c69f266.png" alt="" /></span></div></div><div class="answer_list"><ul class="list_answer "><li><div class="answer_btn"><button class="button" data-weight="1,1,1,1,1" data-pick="parsed-questions-9-answer-0-text" data-pick-selector="p"><p>매우 그렇다</p></button></div></li><li><div class="answer_btn"><button class="button" data-weight="1,1,1,1" data-pick="parsed-questions-9-answer-1-text" data-pick-selector="p"><p>그렇다</p></button></div></li><li><div class="answer_btn"><button class="button" data-weight="1,1,1" data-pick="parsed-questions-9-answer-2-text" data-pick-selector="p"><p>보통이다</p></button></div></li><li><div class="answer_btn"><button class="button" data-weight="1,1" data-pick="parsed-questions-9-answer-3-text" data-pick-selector="p"><p>그렇지 않다</p></button></div></li><li><div class="answer_btn"><button class="button" data-weight="1" data-pick="parsed-questions-9-answer-4-text" data-pick-selector="p"><p>전혀 그렇지 않다</p></button></div></li></ul></div></li><li class="quiz-monkey-question-10"><p class="progress_quiz"><span class="active">1</span><span class="active">2</span><span class="active">3</span><span class="active">4</span><span class="active">5</span><span class="active">6</span><span class="active">7</span><span class="active">8</span><span class="active">9</span><span class="active">10</span><span class="active on">11</span><span>12</span><span>13</span><span>14</span><span>15</span></p><div class="question_header"><div class="question_quiz question_thumb question_thumb2" data-pick="parsed-questions-10-question"><span class="wrap_thumb"><img src="http://t1.daumcdn.net/liveboard/issue/4cfd67b7b15144fa96cf3512f9adb735.png" alt="" /></span></div></div><div class="answer_list"><ul class="list_answer "><li><div class="answer_btn"><button class="button" data-weight="2,2,2,2,2" data-pick="parsed-questions-10-answer-0-text" data-pick-selector="p"><p>매우 그렇다</p></button></div></li><li><div class="answer_btn"><button class="button" data-weight="2,2,2,2" data-pick="parsed-questions-10-answer-1-text" data-pick-selector="p"><p>그렇다</p></button></div></li><li><div class="answer_btn"><button class="button" data-weight="2,2,2" data-pick="parsed-questions-10-answer-2-text" data-pick-selector="p"><p>보통이다</p></button></div></li><li><div class="answer_btn"><button class="button" data-weight="2,2" data-pick="parsed-questions-10-answer-3-text" data-pick-selector="p"><p>그렇지 않다</p></button></div></li><li><div class="answer_btn"><button class="button" data-weight="2" data-pick="parsed-questions-10-answer-4-text" data-pick-selector="p"><p>전혀 그렇지 않다</p></button></div></li></ul></div></li><li class="quiz-monkey-question-11"><p class="progress_quiz"><span class="active">1</span><span class="active">2</span><span class="active">3</span><span class="active">4</span><span class="active">5</span><span class="active">6</span><span class="active">7</span><span class="active">8</span><span class="active">9</span><span class="active">10</span><span class="active">11</span><span class="active on">12</span><span>13</span><span>14</span><span>15</span></p><div class="question_header"><div class="question_quiz question_thumb question_thumb2" data-pick="parsed-questions-11-question"><span class="wrap_thumb"><img src="http://t1.daumcdn.net/liveboard/issue/3811585c3c96462c8766de3259007db3.png" alt="" /></span></div></div><div class="answer_list"><ul class="list_answer "><li><div class="answer_btn"><button class="button" data-weight="0,0,0,0,0" data-pick="parsed-questions-11-answer-0-text" data-pick-selector="p"><p>매우 그렇다</p></button></div></li><li><div class="answer_btn"><button class="button" data-weight="0,0,0,0" data-pick="parsed-questions-11-answer-1-text" data-pick-selector="p"><p>그렇다</p></button></div></li><li><div class="answer_btn"><button class="button" data-weight="0,0,0" data-pick="parsed-questions-11-answer-2-text" data-pick-selector="p"><p>보통이다</p></button></div></li><li><div class="answer_btn"><button class="button" data-weight="0,0" data-pick="parsed-questions-11-answer-3-text" data-pick-selector="p"><p>그렇지 않다</p></button></div></li><li><div class="answer_btn"><button class="button" data-weight="0" data-pick="parsed-questions-11-answer-4-text" data-pick-selector="p"><p>전혀 그렇지 않다</p></button></div></li></ul></div></li><li class="quiz-monkey-question-12"><p class="progress_quiz"><span class="active">1</span><span class="active">2</span><span class="active">3</span><span class="active">4</span><span class="active">5</span><span class="active">6</span><span class="active">7</span><span class="active">8</span><span class="active">9</span><span class="active">10</span><span class="active">11</span><span class="active">12</span><span class="active on">13</span><span>14</span><span>15</span></p><div class="question_header"><div class="question_quiz question_thumb question_thumb2" data-pick="parsed-questions-12-question"><span class="wrap_thumb"><img src="http://t1.daumcdn.net/liveboard/issue/0e692895ce4b4e87b01e73922be88d4e.png" alt="" /></span></div></div><div class="answer_list"><ul class="list_answer "><li><div class="answer_btn"><button class="button" data-weight="1,1,1,1,1" data-pick="parsed-questions-12-answer-0-text" data-pick-selector="p"><p>매우 그렇다</p></button></div></li><li><div class="answer_btn"><button class="button" data-weight="1,1,1,1" data-pick="parsed-questions-12-answer-1-text" data-pick-selector="p"><p>그렇다</p></button></div></li><li><div class="answer_btn"><button class="button" data-weight="1,1,1" data-pick="parsed-questions-12-answer-2-text" data-pick-selector="p"><p>보통이다</p></button></div></li><li><div class="answer_btn"><button class="button" data-weight="1,1" data-pick="parsed-questions-12-answer-3-text" data-pick-selector="p"><p>그렇지 않다</p></button></div></li><li><div class="answer_btn"><button class="button" data-weight="1" data-pick="parsed-questions-12-answer-4-text" data-pick-selector="p"><p>전혀 그렇지 않다</p></button></div></li></ul></div></li><li class="quiz-monkey-question-13"><p class="progress_quiz"><span class="active">1</span><span class="active">2</span><span class="active">3</span><span class="active">4</span><span class="active">5</span><span class="active">6</span><span class="active">7</span><span class="active">8</span><span class="active">9</span><span class="active">10</span><span class="active">11</span><span class="active">12</span><span class="active">13</span><span class="active on">14</span><span>15</span></p><div class="question_header"><div class="question_quiz question_thumb question_thumb2" data-pick="parsed-questions-13-question"><span class="wrap_thumb"><img src="http://t1.daumcdn.net/liveboard/issue/774bca1a96a24bd2aee7efb3dc4bde9f.png" alt="" /></span></div></div><div class="answer_list"><ul class="list_answer "><li><div class="answer_btn"><button class="button" data-weight="2" data-pick="parsed-questions-13-answer-0-text" data-pick-selector="p"><p>매우 그렇다</p></button></div></li><li><div class="answer_btn"><button class="button" data-weight="2,2" data-pick="parsed-questions-13-answer-1-text" data-pick-selector="p"><p>그렇다</p></button></div></li><li><div class="answer_btn"><button class="button" data-weight="2,2,2" data-pick="parsed-questions-13-answer-2-text" data-pick-selector="p"><p>보통이다</p></button></div></li><li><div class="answer_btn"><button class="button" data-weight="2,2,2,2" data-pick="parsed-questions-13-answer-3-text" data-pick-selector="p"><p>그렇지 않다</p></button></div></li><li><div class="answer_btn"><button class="button" data-weight="2,2,2,2,2" data-pick="parsed-questions-13-answer-4-text" data-pick-selector="p"><p>전혀 그렇지 않다</p></button></div></li></ul></div></li><li class="quiz-monkey-question-14"><p class="progress_quiz"><span class="active">1</span><span class="active">2</span><span class="active">3</span><span class="active">4</span><span class="active">5</span><span class="active">6</span><span class="active">7</span><span class="active">8</span><span class="active">9</span><span class="active">10</span><span class="active">11</span><span class="active">12</span><span class="active">13</span><span class="active">14</span><span class="active on">15</span></p><div class="question_header"><div class="question_quiz question_thumb question_thumb2" data-pick="parsed-questions-14-question"><span class="wrap_thumb"><img src="http://t1.daumcdn.net/liveboard/issue/a2cbfc8b98d74fb4b0344a1c8e23df97.png" alt="" /></span></div></div><div class="answer_list"><ul class="list_answer "><li><div class="answer_btn"><button class="button" data-weight="0,0,0,0,0" data-pick="parsed-questions-14-answer-0-text" data-pick-selector="p"><p>매우 그렇다</p></button></div></li><li><div class="answer_btn"><button class="button" data-weight="0,0,0,0" data-pick="parsed-questions-14-answer-1-text" data-pick-selector="p"><p>그렇다</p></button></div></li><li><div class="answer_btn"><button class="button" data-weight="0,0,0" data-pick="parsed-questions-14-answer-2-text" data-pick-selector="p"><p>보통이다</p></button></div></li><li><div class="answer_btn"><button class="button" data-weight="0,0" data-pick="parsed-questions-14-answer-3-text" data-pick-selector="p"><p>그렇지 않다</p></button></div></li><li><div class="answer_btn"><button class="button" data-weight="0" data-pick="parsed-questions-14-answer-4-text" data-pick-selector="p"><p>전혀 그렇지 않다</p></button></div></li></ul></div></li></ul></div><div class="quiz-monkey-result quiztype-0"><div class="quizmon-loading"></div><ul class="list_quiz list_result"><li class="quiz-monkey-result-0" data-result-key="0"><strong class="result_quiz" data-pick="parsed-results-0-title" data-pick-type="text">당신의 연애유형은 &quot;미인형&quot;입니다.</strong><div class="result_text" data-pick="parsed-results-0-text"><p><span class="wrap_thumb"><img src="/static/images/yeonsu.png" alt="" /></span></p><span style="font-size:.9em;line-height:1.4em;"></span><b style="font-size:1.2em;"><br />미인형(juicy)이란?</b><br><br>이 유형이 미인형(juicy)’으로 불리는 이유는 너무나도 아름답기 때문이에요. 미인형 연애유형을 가진 사람들은 상대방으로부터 항상 많은 애정을 받을 수 있기 때문에 앞으로 항상 행복한 날만이 기다리고 있어요.<br><br><br><b style="font-size:1.2em;">미인형의 연애스타일</b><br><br>1) 미인형은 일단 연애를 시작하게 되면 상대방에게 넘치는 애정을 받는 경향이 있어요. 상대방이 간혹 집착할 수도 있어요. 서로가 서로에게 사랑을 표현하면 지금보다 앞으로 더욱 행복해 질 수 있어요.<br><br>2) 미인형은 오늘 최고로 행복한 생일을 맞게 될거에요.<br><br> 자기야♡<br> 나랑 처음으로 같이 보내는 자기 생일이에요 생일 너무 축하해♡♡<br>사실 내가 이 사이트 만드느라 생일 카드를 못썼어ㅎ... 이쁘게 봐주구ㅎ_ㅎ<br>내가 처음 자기를 만났을땐 표현도 서툴고 많이 어색했는데 자길 만나면서 성격이 나도 모르게 많이 변하는것같아<br>나 엄청 나밖에 생각 안하는 이기적인 사람이었는데 이제는 자기밖에 모르는 사람이 됐어 <br>자기가 좋아하면 나도 기분이 좋고 자기가 슬퍼하면 나도 같이 슬퍼지는데 많은 감정을 같이 공유하고 있다는게 느껴져서 너무 좋아<br>요즘 매일매일 행복하게 해줘서 고마워. 자기는 내 비타민이야^^<br>오늘 하루도 행복하게 해줄게 이따봐요 ♡^3^♡ 쥬스♡<br><br><br><b style="font-size:1.2em;">주의사항</b><br><br>사랑을 많이많이 표현하세요. 이따 볼거에요.<br><br><br><b style="font-size:1.2em;">우리의 연애궁합은?</b><br><br>친구나 애인의 애착유형이 궁금하신가요? 일상적인 행동과 말투를 통해 다른 사람의 애착유형 또한 정확하게 알아볼 수 있습니다. 자신과 상대방의 연애스타일에 따른 궁합 알아보고 싶다면 <a href="http://goo.gl/zZQ6yZ" target="_blank">[애착유형 테스트 풀버전]</a>을 무료로 해보세요. 당신의 연애 궁합을 가장 정확하게 알려드립니다.<div><a href="http://goo.gl/zZQ6yZ" target="_blank">[애착유형 테스트 풀버젼 해보기]</a></div></div></li><li class="quiz-monkey-result-1" data-result-key="1"><strong class="result_quiz" data-pick="parsed-results-1-title" data-pick-type="text">당신의 연애유형은 &quot;미인형&quot;입니다.</strong><div class="result_text" data-pick="parsed-results-0-text"><p><span class="wrap_thumb"><img src="/static/images/yeonsu.png" alt="" /></span></p><span style="font-size:.9em;line-height:1.4em;"></span><b style="font-size:1.2em;"><br />미인형(juicy)이란?</b><br><br>이 유형이 미인형(juicy)’으로 불리는 이유는 너무나도 아름답기 때문이에요. 미인형 연애유형을 가진 사람들은 상대방으로부터 항상 많은 애정을 받을 수 있기 때문에 앞으로 항상 행복한 날만이 기다리고 있어요.<br><br><br><b style="font-size:1.2em;">미인형의 연애스타일</b><br><br>1) 미인형은 일단 연애를 시작하게 되면 상대방에게 넘치는 애정을 받는 경향이 있어요. 상대방이 간혹 집착할 수도 있어요. 서로가 서로에게 사랑을 표현하면 지금보다 앞으로 더욱 행복해 질 수 있어요.<br><br>2) 미인형은 오늘 최고로 행복한 생일을 맞게 될거에요.<br><br> 자기야♡<br> 나랑 처음으로 같이 보내는 자기 생일이에요 생일 너무 축하해♡♡<br>사실 내가 이 사이트 만드느라 생일 카드를 못썼어ㅎ... 이쁘게 봐주구ㅎ_ㅎ<br>내가 처음 자기를 만났을땐 표현도 서툴고 많이 어색했는데 자길 만나면서 성격이 나도 모르게 많이 변하는것같아<br>나 엄청 나밖에 생각 안하는 이기적인 사람이었는데 이제는 자기밖에 모르는 사람이 됐어 <br>자기가 좋아하면 나도 기분이 좋고 자기가 슬퍼하면 나도 같이 슬퍼지는데 많은 감정을 같이 공유하고 있다는게 느껴져서 너무 좋아<br>요즘 매일매일 행복하게 해줘서 고마워. 자기는 내 비타민이야^^<br>오늘 하루도 행복하게 해줄게 이따봐요 ♡^3^♡ 쥬스♡<br><br><br><b style="font-size:1.2em;">주의사항</b><br><br>사랑을 많이많이 표현하세요. 이따 볼거에요.<br><br><br><b style="font-size:1.2em;">우리의 연애궁합은?</b><br><br>친구나 애인의 애착유형이 궁금하신가요? 일상적인 행동과 말투를 통해 다른 사람의 애착유형 또한 정확하게 알아볼 수 있습니다. 자신과 상대방의 연애스타일에 따른 궁합 알아보고 싶다면 <a href="http://goo.gl/zZQ6yZ" target="_blank">[애착유형 테스트 풀버전]</a>을 무료로 해보세요. 당신의 연애 궁합을 가장 정확하게 알려드립니다.<div><a href="http://goo.gl/zZQ6yZ" target="_blank">[애착유형 테스트 풀버젼 해보기]</a></div></div></li><li class="quiz-monkey-result-2" data-result-key="2"><strong class="result_quiz" data-pick="parsed-results-2-title" data-pick-type="text">당신의 연애유형은 &quot;미인형&quot;입니다.</strong><div class="result_text" data-pick="parsed-results-0-text"><p><span class="wrap_thumb"><img src="/static/images/yeonsu.png" alt="" /></span></p><span style="font-size:.9em;line-height:1.4em;"></span><b style="font-size:1.2em;"><br />미인형(juicy)이란?</b><br><br>이 유형이 미인형(juicy)’으로 불리는 이유는 너무나도 아름답기 때문이에요. 미인형 연애유형을 가진 사람들은 상대방으로부터 항상 많은 애정을 받을 수 있기 때문에 앞으로 항상 행복한 날만이 기다리고 있어요.<br><br><br><b style="font-size:1.2em;">미인형의 연애스타일</b><br><br>1) 미인형은 일단 연애를 시작하게 되면 상대방에게 넘치는 애정을 받는 경향이 있어요. 상대방이 간혹 집착할 수도 있어요. 서로가 서로에게 사랑을 표현하면 지금보다 앞으로 더욱 행복해 질 수 있어요.<br><br>2) 미인형은 오늘 최고로 행복한 생일을 맞게 될거에요.<br><br> 자기야♡<br> 나랑 처음으로 같이 보내는 자기 생일이에요 생일 너무 축하해♡♡<br>사실 내가 이 사이트 만드느라 생일 카드를 못썼어ㅎ... 이쁘게 봐주구ㅎ_ㅎ<br>내가 처음 자기를 만났을땐 표현도 서툴고 많이 어색했는데 자길 만나면서 성격이 나도 모르게 많이 변하는것같아<br>나 엄청 나밖에 생각 안하는 이기적인 사람이었는데 이제는 자기밖에 모르는 사람이 됐어 <br>자기가 좋아하면 나도 기분이 좋고 자기가 슬퍼하면 나도 같이 슬퍼지는데 많은 감정을 같이 공유하고 있다는게 느껴져서 너무 좋아<br>요즘 매일매일 행복하게 해줘서 고마워. 자기는 내 비타민이야^^<br>오늘 하루도 행복하게 해줄게 이따봐요 ♡^3^♡ 쥬스♡<br><br><br><b style="font-size:1.2em;">주의사항</b><br><br>사랑을 많이많이 표현하세요. 이따 볼거에요.<br><br><br><b style="font-size:1.2em;">우리의 연애궁합은?</b><br><br>친구나 애인의 애착유형이 궁금하신가요? 일상적인 행동과 말투를 통해 다른 사람의 애착유형 또한 정확하게 알아볼 수 있습니다. 자신과 상대방의 연애스타일에 따른 궁합 알아보고 싶다면 <a href="http://goo.gl/zZQ6yZ" target="_blank">[애착유형 테스트 풀버전]</a>을 무료로 해보세요. 당신의 연애 궁합을 가장 정확하게 알려드립니다.</p><p><a href="http://goo.gl/zZQ6yZ" target="_blank">[애착유형 테스트 풀버젼 해보기]</a></p></div></li></ul><p class="counter"><span>1</span>명이 참여하였습니다.</p><button class="btn_quiz reset" data-label="다시하기|나도하기">다시하기</button></div>',
			css = '<style>@charset \"utf-8\";/* reset */.quiz-monkey div, .quiz-monkey dl, .quiz-monkey dt, .quiz-monkey dd, .quiz-monkey ul, .quiz-monkey ol, .quiz-monkey li, .quiz-monkey h1, .quiz-monkey h2, .quiz-monkey h3, .quiz-monkey h4, .quiz-monkey h5, .quiz-monkey h6, .quiz-monkey pre, .quiz-monkey code, .quiz-monkey form, .quiz-monkey fieldset, .quiz-monkey legend, .quiz-monkey textarea, .quiz-monkey p, .quiz-monkey blockquote, .quiz-monkey th, .quiz-monkey td, .quiz-monkey input, .quiz-monkey select, .quiz-monkey textarea, .quiz-monkey button{margin:0;padding:0}.quiz-monkey fieldset, .quiz-monkey img{border:0 none}.quiz-monkey dl, .quiz-monkey ul, .quiz-monkey ol, .quiz-monkey menu, .quiz-monkey li{list-style:none}.quiz-monkey blockquote, .quiz-monkey q{quotes:none}.quiz-monkey blockquote:before, .quiz-monkey blockquote:after, .quiz-monkey q:before, .quiz-monkey  q:after{content:\'\';content:none}.quiz-monkey input, .quiz-monkey select, .quiz-monkey textarea, .quiz-monkey button{vertical-align:middle;font-size:100%}.quiz-monkey button{border:0 none;background-color:transparent;cursor:pointer}.quiz-monkey table{border-collapse:collapse;border-spacing:0}.quiz-monkey input:checked[type=\'checkbox\']{background-color:#666; -webkit-appearance:checkbox}.quiz-monkey input[type=\'text\'], .quiz-monkey input[type=\'password\'], .quiz-monkey input[type=\'submit\'], .quiz-monkey input[type=\'search\'], .quiz-monkey input[type=\'tel\'], .quiz-monkey input[type=\'email\'], .quiz-monkey input[type=\'button\'], .quiz-monkey input[type=\'reset\']{-webkit-appearance:none;border-radius:0}.quiz-monkey input[type=\'search\']::-webkit-search-cancel-button{-webkit-appearance:none}.quiz-monkey th, .quiz-monkey td, .quiz-monkey input, .quiz-monkey select, .quiz-monkey textarea, .quiz-monkey button{font-size:14px;line-height:1.5;font-family:\'Noto Sans light\', sans-serif;color:#27282d;letter-spacing:-1px} /* color값은 디자인가이드에 맞게사용 */ .quiz-monkey a{color:#3898d5;text-decoration:none}.quiz-monkey a:active,.quiz-monkey a:hover,.quiz-monkey a:focus{text-decoration:underline}.quiz-monkey .hint a,.quiz-monkey .hint a:active,.quiz-monkey .hint a:hover,.quiz-monkey .hint a:focus{color:#fff}.quiz-monkey address, .quiz-monkey caption, .quiz-monkey cite, .quiz-monkey code, .quiz-monkey dfn, .quiz-monkey em, .quiz-monkey var{font-style:normal;font-weight:normal}/* global */.quiz-monkey .ir_pm{display:block;overflow:hidden;font-size:0px;line-height:0;text-indent:-9999px} /* 사용된 이미지내 의미있는 텍스트의 대체텍스트를 제공할때 */.quiz-monkey .ir_wa{display:block;overflow:hidden;position:relative;z-index:-1;width:100%;height:100%} /* 중요한 이미지 대체텍스트로 이미지off시에도 대체 텍스트를 보여주고자 할때 */.quiz-monkey .screen_out{overflow:hidden;position:absolute;width:0;height:0;line-height:0;text-indent:-9999px} /* 대체텍스트가 아닌 접근성을 위한 숨김텍스트를 제공할때 *//* 공통 */.quiz-monkey .quiz-monkey-question,.quiz-monkey .quiz-monkey-result{display:none}.quiz-monkey.show-question .quiz-monkey-question{display:block}.quiz-monkey.show-result .quiz-monkey-result{display:block}.quiz-monkey .wrap_thumb{display:block;overflow:hidden;position:relative}.quiz-monkey .wrap_thumb:after{position:absolute;top:0;left:0;z-index:10;width:100%;height:100%;border:1px solid rgba(0,0,0,0.1);box-sizing:border-box;content:\'\'}.quiz-monkey img{display:block;width:100%;margin:0 auto}.quiz-monkey .btn_quiz{display:block;width:100%;height:52px;border:1px solid #00c99d;border-radius:30px;font-size:18px;line-height:50px;color:#00c596;background-color:#fff;box-sizing:border-box;text-align:center}.quiz-monkey .btn_quiz:hover{color:#fff;background-color:#00c99d}.quiz-monkey{overflow:hidden}.quiz-monkey:before{display:block;width:46px;height:2px;border-top:2px solid #000;content:\"\"}.quiz-monkey .tit_quiz{display:block;margin:24px 0 29px;font-size:32px;line-height:40px;letter-spacing:-1px}.quiz-monkey .list_quiz li{display:none}.quiz-monkey .list_quiz .on{display:list-item}.quiz-monkey .intro_quiz{margin-bottom:29px}.quiz-monkey .intro_quiz p{font-size:20px;line-height:32px;letter-spacing:-1px}.quiz-monkey .counter{visibility:hidden;clear:both;text-align:center;margin:0.6em 0}.quiz-monkey .quiztype-1 .counter{text-align:right}.quiz-monkey .quiz-monkey-result.quiztype-1 .counter{text-align:center}.quiz-monkey .counter.on{visibility:visible}.quiz-monkey .counter span{color:#00c99d}.quiz-monkey-result.loading .counter.on{visibility:hidden}.quiz-monkey-result .counter.on{visibility:visible}.quiz-monkey .progress_quiz{overflow:hidden;width:100%;margin-bottom:22px}.quiz-monkey .progress_quiz span{float:left;width:28px;height:22px;padding-top:2px;margin-right:4px;border-bottom:2px solid #dadbe1;font-size:18px;line-height:20px;font-family:Helvetica;color:#aeb1b7;text-align:center}.quiz-monkey .progress_quiz .on{overflow:hidden;height:24px;padding-top:0;border-color:#00c99d;font-size:0;line-height:0;background:url(http://m1.daumcdn.net/img-media/1boon/pc/ico_progress.png) 50% 0 no-repeat;text-indent:-9999px}.quiz-monkey .tit_question{display:block;margin-bottom:11px;font-size:20px;letter-spacing:-1px}.quiz-monkey .question_header{position:relative}.quiz-monkey .question_quiz .wrap_thumb{margin-top:16px}.quiz-monkey .question_thumb{position:relative}.quiz-monkey .question_thumb .tit_question{position:absolute;bottom:28px;left:0;right:0;z-index:10;padding:0 26px;margin-bottom:0;color:#fff}.quiz-monkey .question_thumb .wrap_thumb:before{position:absolute;bottom:0;left:0;width:100%;height:100%;background:-webkit-gradient(linear, left top, left bottom, color-stop(40%,rgba(39,40,45,0)), color-stop(100%,rgba(39,40,45,0.8)));background:-moz-linear-gradient(top,  rgba(39,40,45,0) 40%, rgba(39,40,45,0.8) 100%);background:-o-linear-gradient(top,  rgba(39,40,45,0) 40%,rgba(39,40,45,0.8) 100%);background:linear-gradient(to bottom,  rgba(39,40,45,0) 40%,rgba(39,40,45,0.8) 100%);content:\'\'}.quiz-monkey .question_thumb2 .wrap_thumb:before{display:none}.quiz-monkey .answer_list{position:relative}.quiz-monkey .list_answer{overflow:hidden}.quiz-monkey .list_answer li{display:list-item;margin-top:12px}.quiz-monkey .list_answer .button{display:block;width:100%;position:relative;height:65px;vertical-align:middle;padding:0 26px;font-size:18px;line-height:1.5;background-color:#fff;letter-spacing:-1px;text-align:left;box-sizing:border-box}.quiz-monkey .list_answer .button:after{position:absolute;top:0;left:0;z-index:10;width:100%;height:100%;border:1px solid rgba(0,0,0,0.1);box-sizing:border-box;content:\'\'}.quiz-monkey .list_answer button:hover{color:#fff;background-color:#00c99d}.quiz-monkey .list_result .on ul{padding-left:22px}.quiz-monkey .list_result .on li{display:list-item;font-size:20px;line-height:32px;list-style:disc}.quiz-monkey .length3, .quiz-monkey .length7{margin:0 -6px}.quiz-monkey .length3 li, .quiz-monkey .length7 li{float:left}.quiz-monkey .length3 li{width:33.33%}.quiz-monkey .length7 li{width:50%}.quiz-monkey .thumb li{width:33.33%}.quiz-monkey .length3 .answer_btn, .quiz-monkey .length7 .answer_btn{margin:0 6px}.quiz-monkey .length3 .button, .quiz-monkey .length7 .button{text-align:center}.quiz-monkey .thumb .wrap_thumb, .quiz-monkey .thumb2 .wrap_thumb{overflow:hidden;height:152px;background-size:cover;background-position:50% 50%}.quiz-monkey .thumb .button{overflow:hidden;height:auto;padding:0}.quiz-monkey .thumb .button .wrap_thumb:after{border:0 none}.quiz-monkey .thumb button:hover .wrap_thumb:after{border:0 none;background-color:#01c99d;background-color:rgba(1, 201, 157, 0.8)}.quiz-monkey .thumb .ico_check{overflow:hidden;position:absolute;top:-50%;left:-50%;z-index:20;width:37px;height:37px;margin:-19px 0 0 -19px;font-size:0;line-height:0;background:url(http://m1.daumcdn.net/img-media/1boon/pc/ico_quiz.png) 0 -120px no-repeat;text-indent:-9999px}.quiz-monkey .thumb button:hover .ico_check{top:50%;left:50%}.quiz-monkey .thumb2 .button{overflow:hidden;height:217px;padding:152px 26px 0}.quiz-monkey .thumb2 .button .wrap_thumb{position:absolute;top:0;left:0;right:0}.quiz-monkey .thumb2 .button .wrap_thumb:after{border:0 none;border-bottom:1px solid rgba(0, 0, 0, 0.1)}.quiz-monkey .thumb2 .wrong .wrap_thumb:after{border:5px solid rgb(255, 94, 59)}.quiz-monkey .thumb2 .correct .wrap_thumb:after{border:5px solid rgb(1, 201, 157)}.quiz-monkey .answered .list_answer button:hover{color:#27282d;background-color:#fff}.quiz-monkey .answered .list_answer .correct, .quiz-monkey .answered .list_answer .on{border-color:#00c99d;color:#fff;background-color:#00c99d}.quiz-monkey .answered .list_answer .correct:hover, .quiz-monkey .answered .list_answer .on:hover{border-color:#00c99d;color:#fff;background-color:#00c99d}.quiz-monkey .answered .list_answer .wrong{border-color:#ff5e3b;color:#fff;background-color:#ff5e3b}.quiz-monkey .answered .list_answer .wrong:hover{border-color:#ff5e3b;color:#fff;background-color:#ff5e3b}.quiz-monkey .answered .thumb button:hover .wrap_thumb:after{display:none}.quiz-monkey .answered .thumb button:hover .ico_check{display:none}.quiz-monkey .answered .thumb .correct .wrap_thumb:after, .quiz-monkey .answered .thumb .on .wrap_thumb:after{background-color:rgba(1, 201, 157, 0.8)}.quiz-monkey .answered .thumb .on .ico_check{display:block;top:50%;left:50%}.quiz-monkey .answered .thumb .correct:hover .wrap_thumb:after, .quiz-monkey .answered .thumb .on:hover .wrap_thumb:after{display:block;background-color:rgba(1, 201, 157, 0.8)}.quiz-monkey .answered .thumb .on:hover .ico_check{display:block}.quiz-monkey .answered .thumb .wrong .wrap_thumb:after{background-color:rgba(255, 94, 59, 0.8)}.quiz-monkey .answered .thumb .wrong:hover .wrap_thumb:after{display:block;background-color:rgba(255, 94, 59, 0.8)}.quiz-monkey .hint{display:none;position:absolute;bottom:-7px;right:0;left:0;z-index:50;padding:12px;background-color:#5238f4;background-color:rgba(82, 56, 244, 0.8);font-size:18px;line-height:24px;color:#fff;opacity:0;filter:alpha(opacity=0);transition:opacity 0.3s}.quiz-monkey .question_thumb .hint{bottom:0}.quiz-monkey .answered .hint{display:block;opacity:1;filter:alpha(opacity=100)}.quiz-monkey-result{display:none}.quiz-monkey-result.on{display:block}.quiz-monkey .result_quiz{display:block;margin-bottom:30px;font-weight:bold;font-size:20px;line-height:22px;letter-spacing:-1px}.quiz-monkey .result_quiz .num_result{font-size:50px;line-height:52px}.quiz-monkey .result_text {font-size:20px;line-height:32px}.quiz-monkey .quiz-monkey-share{overflow:hidden;width:240px;margin:26px auto 0}.quiz-monkey .quiz-monkey-share a{float:left;overflow:hidden;width:50px;height:50px;margin:0 5px;border-bottom:0 none;font-size:0;line-height:0;background:url(http://m1.daumcdn.net/img-media/1boon/pc/ico_quiz.png) 0 0 no-repeat;text-indent:-9999px}.quiz-monkey .quiz-monkey-share .\\#kakaostory{background-position:-60px 0}.quiz-monkey .quiz-monkey-share .\\#facebook{background-position:0 -60px}.quiz-monkey .quiz-monkey-share .\\#twitter{background-position:-60px -60px}.quiz-monkey .quiz-monkey-result .link_share{display:none}.quiz-monkey .go-result{display:none;position:fixed;bottom:0;left:0;z-index:9999}.quiz-monkey .go-result.on{display:block}.quiz-monkey .reset{margin-top:30px}.quiz-monkey.show-result .reset{display:block}.quiz-monkey-result.loading .reset{display:none}.quiz-monkey-result .quizmon-loading{display: none;background: url(http://t1.daumcdn.net/quizmon/img/loading.png);background-size: auto 125px;width: 100px;height: 125px;margin: 150px auto}.quiz-monkey-result.loading .quizmon-loading{display: block}.quiz-monkey .quiztype-1 .list_quiz li{display:block;position:relative}.quiz-monkey .quiztype-1 .intro{display:none}.quiz-monkey .quiztype-1 .progress_quiz{margin-top:60px}.quiz-monkey .quiztype-1 .result_quiz{margin-top:60px}.quiz-monkey .quiztype-1 .list_result li{display:none}.quiz-monkey .quiztype-1 .list_result .on{display:block}.quiz-monkey .quiztype-1 .reset{display:none}.section_quiz .quiz-monkey{max-width:600px}/* 모바일 대응 */@media only screen and (max-width: 740px){.quiz-monkey .btn_quiz{height:36px;font-size:14px;line-height:34px}.quiz-monkey .tit_quiz{margin:15px 0 14px;font-size:20px;line-height:27px}.quiz-monkey .intro_quiz{margin-bottom:16px}.quiz-monkey .intro_quiz .wrap_thumb{height:auto;margin-bottom:16px}.quiz-monkey .intro_quiz p{font-size:16px;line-height:26px}.quiz-monkey .progress_quiz{margin-bottom:17px}.quiz-monkey .progress_quiz span{width:21px;height:15px;padding-top:2px;margin-right:2px;font-size:13px;line-height:15px}.quiz-monkey .progress_quiz .on{height:17px;padding-top:0;background:url(http://m1.daumcdn.net/img-media/1boon/m320/ico_progress.png) 50% 0 no-repeat}.quiz-monkey .tit_question{font-size:16px}.quiz-monkey .question_quiz .wrap_thumb{height:auto;margin-top:18px}.quiz-monkey .quiztype-0 .question_thumb .tit_question{bottom:14px;padding:0 13px}.quiz-monkey .quiztype-0 .question_thumb .wrap_thumb:before{background:-webkit-gradient(linear, left top, left bottom, color-stop(40%,rgba(39,40,45,0)), color-stop(100%,rgba(39,40,45,0.8)));background:-moz-linear-gradient(top,  rgba(39,40,45,0) 40%, rgba(39,40,45,0.8) 100%);background:-o-linear-gradient(top,  rgba(39,40,45,0) 40%,rgba(39,40,45,0.8) 100%);background:linear-gradient(to bottom,  rgba(39,40,45,0) 40%,rgba(39,40,45,0.8) 100%)}.quiz-monkey .list_answer li{margin-top:10px}.quiz-monkey .list_answer .button{height:64px;padding:0 13px;font-size:14px;line-height:1.5;-webkit-transition-delay:0.5s;transition-delay:0.5s}.quiz-monkey .length3, .quiz-monkey .length7{margin:0 -5px}.quiz-monkey .thumb li{width:50%}.quiz-monkey .length3 .answer_btn, .quiz-monkey .length7 .answer_btn{margin:0 5px}.quiz-monkey .thumb .button{height:110px;padding:0}.quiz-monkey .thumb2 .button{height:174px;padding:110px 13px 0}.quiz-monkey .thumb .wrap_thumb, .quiz-monkey .thumb2 .wrap_thumb{height:110px}.quiz-monkey .thumb .ico_check{width:28px;height:28px;margin:-14px 0 0 -14px;background:url(http://m1.daumcdn.net/img-media/1boon/m320/ico_quiz.png) 0 -68px no-repeat}.quiz-monkey .hint{font-size:14px;line-height:20px}.quiz-monkey .result_quiz{margin-bottom:18px;font-size:16px;line-height:18px}.quiz-monkey .list_result p{font-size:16px;line-height:26px}.quiz-monkey .list_result .wrap_thumb{height:auto;margin:17px 0 16px}.quiz-monkey .result_text {font-size:16px;line-height:26px}.quiz-monkey .list_result .on li{font-size:16px;line-height:26px}.quiz-monkey .quiz-monkey-share{width:185px;margin:18px auto 0}.quiz-monkey .quiz-monkey-share a{width:32px;height:32px;margin:0 7px;background:url(http://m1.daumcdn.net/img-media/1boon/m320/ico_quiz.png) 0 0 no-repeat}.quiz-monkey .quiz-monkey-share .\\#kakaostory{background-position:-34px 0}.quiz-monkey .quiz-monkey-share .\\#facebook{background-position:0 -34px}.quiz-monkey .quiz-monkey-share .\\#twitter{background-position:-34px -34px}.quiz-monkey .quiz-monkey-result .link_share{display:block;overflow:hidden;width:185px;height:32px;margin:16px auto 0;border-radius:32px;background-color:#ffeb00}.quiz-monkey .quiz-monkey-result .txt_share{display:block;overflow:hidden;width:146px;height:20px;margin:6px auto 0;font-size:0;line-height:0;background:url(http://m1.daumcdn.net/img-media/1boon/m320/share_talk2_160621.png) 0 0 no-repeat;text-indent:-9999px}.quiz-monkey .reset{margin-top:20px}.quiz-monkey .quiztype-1 .progress_quiz{margin-top:40px}.quiz-monkey .quiztype-1 .result_quiz{margin-top:40px}.quiz-monkey .result_quiz .num_result{font-size:39px;line-height:41px}}/* 고해상도 이미지  */@media only screen and (-webkit-min-device-pixel-ratio : 1.5) and (max-width :740px),only screen and (min-device-pixel-ratio : 1.5) and (max-width :740px){.quiz-monkey .progress_quiz .on{background-image:url(http://m1.daumcdn.net/img-media/1boon/m640/ico_progress.png);-webkit-background-size:14px 14px;background-size:14px 14px}.quiz-monkey .thumb .ico_check{background-image:url(http://m1.daumcdn.net/img-media/1boon/m640/ico_quiz.png);-webkit-background-size:68px 98px;background-size:68px 98px}.quiz-monkey .quiz-monkey-share a{background-image:url(http://m1.daumcdn.net/img-media/1boon/m640/ico_quiz.png);-webkit-background-size:68px 98px;background-size:68px 98px}.quiz-monkey .quiz-monkey-result .txt_share{background-image:url(http://m1.daumcdn.net/img-media/1boon/m640/share_talk2_160621.png);-webkit-background-size:146px 20px;background-size:146px 20px}}</style>',
			quizId,
			$el = $('#quizmonkey_1012_1469800065')

		if (html.length > '6') {
			$el.html(html);
			$('head').append(css);
		}

		this.quizType = quizType;
		this.$el = $el;
		this.$question = this.$el.find('.quiz-monkey-question');
		this.$result = this.$el.find('.quiz-monkey-result');
		this.$counter = this.$el.find('.counter');
		this.$window = $(window);
		this.$goResultButton = this.$result.find('.go-result');
		this.quizId = this.getQuizId();
		this.distId = this.getDistId();
		this.resultParameter = 'quizmonkey';

		var result = QueryString.getParameter(window.location.href, this.resultParameter);

		if (result !== undefined) {
			this.showResult(decodeURIComponent(result), true);
			this.scrollToResult();
		} else {
			this.showQuestion();
			this.$question.find('button').on('click', $.proxy(function (event) {
				this.buttonClick(event);
			}, this));
			this.$window.on('scroll', $.proxy(function (event) {
				this.toggleGoResultButton(event);
			}, this));
			this.$goResultButton.on('click', $.proxy(function (event) {
				event.preventDefault();
				this.scrollToResult();
			}, this));
		}

		$(window).on('load', $.proxy(function () {
			if (typeof quizmokeyUtil !== 'undefined') {
				quizmokeyUtil.getCount(this.quizId, $.proxy(function(status, data) {
					if (data > 0) {
						this.$counter.addClass('on');
						this.$counter.find('span').html(data.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","));
					}
				}, this));
			}
		}, this));

		this.loadingAnimation.init(this.$result.find('.quizmon-loading').get(0));
	},

	getQuizId: function () {
		var id = this.$el.attr('id') || 'quizmonkey',
			splited = id.split('_'),
			result;
		if (splited.length == 3) {
			splited.pop();
			result = splited.join('_');
		} else {
			result = id;
		}
		return result;
	},

	getDistId: function () {
		return this.$el.attr('id') || 'quizmonkey';
	},

	isEmbeded: function () {
		return $('.quiz-monkey .quiz-monkey-question, .quiz-monkey .quiz-monkey-result').length !== 2 ? true : false;
	},

	showQuestion: function () {
		this.$el.removeClass('show-result').addClass('show-question').find('li:eq(0)').addClass('on');
	},

	buttonClick: function (event) {
		var $el = $(event.target),
			$questionItem,
			$hintElement,
			$answerList;

		if (!$el.is('button')) {
			$el = $el.parents('button');
		}

		if ($el.parent().is('.card-instruction') || $el.parent().is('.card-answer')) {
			return;
		}

		$questionItem = $el.parents('li[class^=quiz-monkey-question-]');
		$hintElement = $questionItem.find('.hint');
		$answerList = $el.parent().parent();

		if ($el.hasClass('intro')) {
			$questionItem = $el.parent();
			$answerList = null;
		}

		if ($questionItem.hasClass('answered')) {
			return;
		}

		if ($questionItem.find('[data-answer=true]').length > 0) {
			$questionItem.find('[data-answer=true]').addClass('correct');
			if ($el.attr('data-answer') !== 'true') {
				$el.addClass('wrong');
			}
			if ($hintElement.length > 0 && $hintElement.text().length == 0) {
				if ($el.attr('data-answer') !== 'true') {
					if ($questionItem.find('[data-answer=true]').text().length == 0 || $questionItem.find('[data-answer=true]').text() == '선택하기') {
						$hintElement.html('오답입니다.');
					} else {
						$hintElement.html('오답. 정답은 ' + $questionItem.find('[data-answer=true]').text() + '입니다.');
					}
				} else if ($hintElement.html().length == 0) {
					$hintElement.html('정답입니다.');
				}
			}
		} else {
			$hintElement.remove();
		}

		$questionItem.addClass('answered');

		$el.addClass('on');

		this.proceed(event);
	},

	proceed: function (event) {
		var finishQuiz = false,
			$el = $(event.target),
			$currentQuestion = this.$question.find('li.on'),
			$nextQuestiion,
			notAnsweredCount = this.$question.children('ul').children().not('.on').not('.answered').length;

		if (!$el.is('button')) {
			$el = $el.parents('button');
		}

		if (this.quizType === 1) {
			if (notAnsweredCount === 0) {
				this.questionFinished(true);
			}
			return;
		}

		if ($el.data('next') !== undefined) {
			$nextQuestiion = this.$el.find('.quiz-monkey-question-' + $el.data('next'));
			this.createType = 'next';
		} else {
			if (this.createType === 'next') {
				finishQuiz = true;
			}
			$nextQuestiion = $currentQuestion.next();
		}

		$currentQuestion.removeClass('on');

		if ($nextQuestiion.length > 0 && !finishQuiz) {
			$nextQuestiion.addClass('on');
		} else {
			this.questionFinished();
		}

		this.setScrollPosition();
	},

	setScrollPosition: function () {
		var top = this.$el.offset().top,
			height = this.$el.outerHeight(),
			scrollTop = this.$window.scrollTop(),
			daumHead2Offset = $('#daumHead2').outerHeight();

		if (top < scrollTop + daumHead2Offset) {
			this.$window.scrollTop(top - daumHead2Offset);
		}
	},

	questionFinished: function (skipLoading) {
		var result = this.getResult();

		if (skipLoading) {
			if (typeof quizmokeyUtil === 'undefined') {
				this.showResult(this.getResult(), false);
				return;
			}

			quizmokeyUtil.sendToKage({
				"quizId": this.quizId
			}, $.proxy(function (status, data) {
				this.showResult(this.getResult(), false);
			}, this));
		} else if (this.$result.find('[data-option]').length > 0) {
			if (typeof quizmokeyUtil === 'undefined') {
				alert('결과 이미지 생성은 1boon에서만 테스트 가능합니다.');
				this.beforeResult(result);
				return;
			}

			quizmokeyUtil.sendToKage(this.getImageOptions(result), $.proxy(function (status, data) {
				if(status===200) {
					this.beforeResult(result, data.query);
				} else {
					alert('오류가 발생하였습니다.');
					this.reset();
				}
			}, this));

			this.loading(result, true);
		} else {
			if (typeof quizmokeyUtil === 'undefined') {
				this.loading(result);
				return;
			}

			quizmokeyUtil.sendToKage({
				"quizId": this.quizId
			}, $.proxy(function (status, data) {
				this.loading(result);
			}, this));
		}
	},

	loading: function (result, wait) {
		this.$el.removeClass('show-question').addClass('show-result');
		this.$result.addClass('loading');
		this.loadingAnimation.showLoading();

		if (wait) {
			return;
		}

		window.setTimeout($.proxy(function () {
			this.beforeResult(result);
		}, this), 1000 + Math.random() * 2000);
	},

	getResult: function () {
		var resultKey;

		if (this.$el.find('[data-answer]').length > 0) {
			resultKey = this.getResultByAnswer();
		} else if (this.$el.find('[data-weight]').length > 0) {
			resultKey = this.getResultByWeight();
		} else if (this.$el.find('[data-point]').length > 0) {
			resultKey = this.getResultByPoint();
		} else {
			resultKey = this.getResultByYesCount();
		}

		return resultKey;
	},

	getResultByPoint: function () {
		var $selectedButton = this.$question.find('button.on').not('.intro'),
			sum = 0,
			resultKey,
			resultKeys = [];

		$selectedButton.each(function (index, item) {
			var point = $(item).attr('data-point') || 0;
			sum += +point;
		});

		this.$result.find('[data-result-key]').each(function (index, item) {
			var point = $(item).attr('data-result-key');
			resultKeys.push(point);
		});

		$.each(resultKeys.sort(function (a, b) {
			return Number(a) - Number(b);
		}).reverse(), function (index, item) {
			if (Number(sum) <= Number(item)) {
				resultKey = String(item);
			}
		});

		return resultKey;
	},

	getResultByWeight: function () {
		var $selectedButton = this.$question.find('button.on'),
			sum = [],
			resultKey;

		$selectedButton.each(function (index, item) {
			var $item = $(item),
				weight = $item.attr('data-weight'),
				weights;

			if (weight == undefined) {
				return;
			}

			weights = weight.split(',');

			$(weights).each(function (index, item) {
				sum[item] = sum[item] + 1 || 1;
			});
		});

		$(sum).each(function (index, item) {
			if (item == undefined) {
				sum[index] = 0;
			}
		});

		resultKey = $.inArray(Math.max.apply(null, sum), sum);

		return resultKey;
	},

	getResultByAnswer: function () {
		var correctAnswerCount, resultKey;

		correctAnswerCount = this.$question.find('.correct.on').not('.wrong').length;

		this.$result.children('ul').children('li').each(function (index, item) {
			var point = $(item).attr('data-result-key');
			if (correctAnswerCount <= point) {
				resultKey = point;
			}
		});

		return resultKey;
	},

	getResultByYesCount: function () {
		var yesCount, resultKey;

		yesCount = this.$question.find('.list_answer li:first-child button.on').length;
		this.$result.children('ul').children('li').each(function (index, item) {
			var point = $(item).attr('data-result-key');
			if (yesCount <= point) {
				resultKey = point;
			}
		});

		return resultKey;
	},

	getImageOptions: function (result) {
		var resultKey = result.split('_')[0],
			$result = this.getResultElement(resultKey),
			image = $result.find('img').attr('src'),
			textOption = $result.attr('data-option'),
			options = {
				"quizId": this.quizId,
				"imageUrl": image,
				"text": [{
					"x": 100,
					"y": 100,
					"msg": result.split('_')[1],
					"size": 30,
					"color": "#ffffff",
					"stroke": "#bbbbbb"
				}]
			};

		if (textOption.length > 0 && textOption.split('_').length == 6) {
			textOption = textOption.split('_');
			options.text[0].x = textOption[0];
			options.text[0].y = textOption[1];
			options.text[0].size = textOption[2];
			options.text[0].color = textOption[3];
			options.text[0].stroke = textOption[4];
			options.text[0].font = textOption[5];
		}

		return options;
	},

	beforeResult: function (result, queryString) {
		if (this.isEmbeded()) {
			// FIXME: queryString에 kage 이미지의 호스트 경로가 없어서 이미지를 표시할 수 없음
			this.showResult(result, true);
			return;
		}

		href = QueryString.addParameter(window.location.href, this.resultParameter, encodeURIComponent(result));
		if (queryString) {
			href = QueryString.addQueryString(href, queryString);
		}

		window.location.href = href;
	},

	getResultElement: function (resultKey) {
		var $selectedResult;
		if (this.$el.find('[data-result-key=' + resultKey + ']').length > 0) {
			$selectedResult = this.$el.find('[data-result-key=' + resultKey + ']');
		} else {
			$selectedResult = this.$el.find('.quiz-monkey-result-' + resultKey);
		}
		return $selectedResult;
	},

	showResult: function (result, hideQuestion) {
		var $resetButton = this.$result.find('.reset'),
			resultKey, userInput;
		var $selectedResult;

		if (hideQuestion) {
			this.$el.removeClass('show-question');
			this.$result.removeClass('loading');
			this.loadingAnimation.hideLoading();
		}
		this.$result.addClass('on');

		$resetButton.on('click', $.proxy(function () {
			this.reset();
		}, this)).html($.proxy(function () {
			var shareServiceName = QueryString.getParameter(window.location.href, 'quizmonkeyref'),
				label = '';

			if (shareServiceName !== undefined) {
				label = $resetButton.data('label').split('|')[1];
			} else {
				label = $resetButton.data('label').split('|')[0];
			}

			return label;
		}, this)).show();

		result = String(result) || '0';
		if (result.indexOf('_') > -1) {
			resultKey = result.split('_')[0];
			userInput = result.split('_')[1];
		} else {
			resultKey = result;
			userInput = '';
		}

		$selectedResult = this.getResultElement(resultKey);

		$selectedResult.addClass('on').find('.placeholder-0').text(decodeURIComponent(userInput));

			if (window.QUIZ_KAGE_IMAGE !== undefined && window.QUIZ_KAGE_IMAGE.length > 0) {
				$selectedResult.find('img').attr('src', window.QUIZ_KAGE_IMAGE);
			}

		this.initShare(resultKey);
		this.toggleGoResultButton();
	},

	toggleGoResultButton: function (event) {
		var scrollTop = this.$window.scrollTop(),
			resultPosition = this.$result.offset().top;

		if (scrollTop + this.$window.height() < resultPosition) {
			this.$goResultButton.addClass('on');
		} else {
			this.$goResultButton.removeClass('on');
		}
	},

	scrollToResult: function () {
		var self = this;
		window.setTimeout(function () {
			self.$window.scrollTop(self.$result.offset().top - 100);
		}, 200);
	},

	reset: function () {
		var href;

		if (this.isEmbeded()) {
			this.$el.find('.answered, .correct, .wrong, .on').removeClass('answered correct wrong on');
			if (this.$el.find('.quiz-monkey-form').length > 0) {
			this.$el.find('.quiz-monkey-form').get(0).reset();
			}
			this.showQuestion();
			this.resetCard && this.resetCard();
			return;
		}

		href = QueryString.removeParameter(window.location.href, this.resultParameter);
		href = QueryString.removeParameter(href, 'qkage');
		href = QueryString.removeParameter(href, 'quizmonkeyref');

		window.location.href = href;
	},

	initShare: function (resultKey) {
		var initialized = false;
		var $resultEl = this.$el.find('.quiz-monkey-result-' + resultKey);
		var link = window.location.href,
			title = (this.$el.find('.tit_quiz').text() + ' ' + $resultEl.find('.result_quiz').text()).replace(/(\r\n|\n|\r)/gm,""),
			description = $resultEl.find('p').text().substring(0, 50) + '...',
			image = $resultEl.find('img').attr('src') || '',
			html = ['<div class="#quiz_monkey_share quiz-monkey-share">'];

		if (initialized || this.isEmbeded()) {
			return;
		}

		if (typeof quizmokeyUtil !== 'object') {
			$(window).on('DOMContentLoaded', $.proxy(function () {
				this.initShare(resultKey);
			}, this));
			return;
		}

		link = QueryString.addParameter(link, this.resultParameter, resultKey);

		$([
			{
				'service': 'kakaotalk',
				'linkText': '카카오톡'
			},
			{
				'service': 'kakaostory',
				'linkText': '카카오스토리',
				'data': {
					'url_info[title]': title,
					'url_info[desc]': description,
					'url_info[imageurl]': image
				}
			},
			{
				'service': 'facebook',
				'linkText': '페이스북',
				'data': {
					'facebook[description]': description,
					'facebook[picture]': image
				}
			},
			{
				'service': 'twitter',
				'linkText': '트위터'
			}
		]).each(function (name, value) {
			var dataText = [];
			var shareLink = QueryString.addParameter(link, 'quizmonkeyref', value.service);

			if (value.data !== undefined) {
				$.each(value.data, function (dataKey, dataValue) {
					dataText.push(' data-' + dataKey + '="' + dataValue + '"');
				});
			}

			html.push('<a href="#none" class="component-share-btn #' + value.service + '"  data-handler="' + value.service + '" data-link="' + shareLink + '" data-prefix="' + title + '"' + dataText.join('') + '>' + value.linkText + '</a>');
		});

		html.push('</div>');

		link = QueryString.addParameter(link, 'quizmonkeyref', 'kakaoprofile');
		html.push('<a href="#none" class="link_share only1boon btn-quiz-talkprofile-badge" data-link="' + link + '"><span class="txt_share">카카오톡 프로필 배지 달기</span></a>');

		$resultEl.append(html.join(' '));

		initialized = true;
	}
};
(new QuizMonkey()).init(0);
})();