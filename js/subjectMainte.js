var subjectMainte = $.extend({
	// 登録ボタン押下で入力文字列をデータストアに追加します
	register: function(e) {
		e.preventDefault();
		var subjectName = $('#subjectName').val();
		// 入力チェック
		if (!subjectName) { 
			alert('文字を入力してください。');
			return;
		}
		$.post('/subject', {'subjectName': subjectName},
				function(data) {
					alert('登録しました');
					var tableTag = $('.allSubjectTable');
					var isExist = tableTag.find('tbody').length === 0 ? false : true;
					if (!isExist) { tableTag.append('<tbody></tbody>'); }
					tableTag.find('tbody').append(data);
					$('#subjectName').val('');
				}, 'html');
		return;
	},
	// 更新ボタン押下で科目名を更新します
	updateSubject: function(e, $_) {
		e.preventDefault();
		var updateKey = $_.attr('name');
		var updateSubjectName = $_.parent().parent().find('#TxtSubjectName').val();
		// 入力チェック
		if (!updateSubjectName) { 
			alert('文字を入力してください。');
			return;
		}
		$.post('/updateSubject', {'updateKey': updateKey, 'updateSubjectName': updateSubjectName},
				function(data) {
					alert('更新しました');
					$_.parent().parent().find('#TxtSubjectName').val(data.subjectName)
				}, 'json');
		return;
	},
	// 削除ボタン押下で科目名を削除します
	deleteSubject: function(e, $_) {
		e.preventDefault();
		if (!confirm('当科目を使用している学習時間データも削除されますがよろしいですか？')) { return; }
		var deleteKey = $_.attr('name');
		$.post('/deleteSubject', {'deleteKey': deleteKey},
				function() {
					alert('削除しました');
					$_.parent().parent().remove();
				}, 'json');
		return;
	}
});

$(document).ready(function() {
	// 登録ボタン
	$('#register').unbind('click').bind('click',function(e){
		var $button = $(this);
		common.btnDisabled($button);
		subjectMainte.register(e);
		common.btnEnabled($button);
		return
	});
	// 更新ボタン
	$('.Js-UpdateSubject').unbind('click').bind('click',function(e){
		var $button = $(this);
		common.btnDisabled($button);
		subjectMainte.updateSubject(e, $(this));
		common.btnEnabled($button);
		return
	});
	// 削除ボタン
	$('.Js-DeleteSubject').unbind('click').bind('click',function(e){
		var $button = $(this);
		common.btnDisabled($button);
		subjectMainte.deleteSubject(e, $(this));
		common.btnEnabled($button);
		return
	});
});



