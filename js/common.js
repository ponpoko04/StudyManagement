var common = $.extend({
	// ボタン押下不可
	btnDisabled: function($button) {
		$button.attr('disabled', true);
	},
	// ボタン押下可
	btnEnabled: function($button) {
		// ３秒待機して復活(スマホのJS処理速度による)
		// GalaxyNoteⅡにてテスト済
		setTimeout(function() { $button.removeAttr("disabled"); }, 3000);
	}
});
