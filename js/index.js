var index = $.extend({
	// 登録ボタン押下で入力文字列をデータストアに追加します
	register: function(e) {
		e.preventDefault();
		var item = $('#item').val();
		var content = $('#content').val();
		var studyTimeYear = $('#studyTimeYear').val();
		var studyTimeMonth = $('#studyTimeMonth').val();
		var studyTimeDay = $('#studyTimeDay').val();
		var studyTimeHour = $('#studyTimeHour').val();
		var studyTimeMinute = $('#studyTimeMinute').val();

		// 入力チェック
		var tmpDate = new Date(studyTimeYear, parseInt(studyTimeMonth, 10) - 1, studyTimeDay);
		if (!(tmpDate.getFullYear() == studyTimeYear &&
			  tmpDate.getMonth() == parseInt(studyTimeMonth, 10) - 1 &&
			  tmpDate.getDate() == studyTimeDay)) {
			alert('選択した日付が正しくありません。');
			return;
		}

		if (studyTimeHour === '00' && studyTimeMinute === '00') {
			alert('時間または分で"00"以外を選択して下さい。');
			return;
		}

		// 送信します
		$.post('/register', {'item': item, 'content': content, 'studyTimeYear': studyTimeYear,
							 'studyTimeMonth': studyTimeMonth, 'studyTimeDay': studyTimeDay,
							 'studyTimeHour': studyTimeHour, 'studyTimeMinute': studyTimeMinute},
				function(data) {
					alert('登録しました');
					var tableTag = $('.totalStudyTimeTable');
					var isExist = tableTag.find('tbody').length === 0 ? false : true;
					if (!isExist) { tableTag.append('<tbody></tbody>'); }
					tableTag.find('tbody').append(data);
					
					// 入力内容の初期化
					$('#item').val($('#item').find('option').eq(1).val());
					$('#content').val('');
					$('#studyTimeYear').val(tmpDate.getFullYear());
					$('#studyTimeMonth').val(('00' + (tmpDate.getMonth() + 1)).slice(-2));
					$('#studyTimeDay').val(tmpDate.getDate());
					$('#studyTimeHour').val('00');
					$('#studyTimeMinute').val('00');
				}, 'html');
		return;
	}
});

$(document).ready(function() {
	// 登録ボタン
	$('#register').unbind('click').bind('click',function(e){
		var $button = $(this);
		common.btnDisabled($button);
		index.register(e);
		common.btnEnabled($button);
		return 
	});
});
