var listPerDate = $.extend({
	// イベント追加
	addClickEvent: function() {
		// クリック日付取得
		$('#calendar').find('.js-cell').off('click').on('click', function(e) {
			var $clickcell = $(this);
			var $clickday = $clickcell.children('.fc-date').eq(0);
			var $calcell = $('#calendar').find('.js-cell');
			
			// 選択セルのスタイル変更
			$calcell.removeClass('selected-cell');
			$calcell.children('.fc-date').removeClass('selected-cell-font');
			$clickcell.addClass('selected-cell');
			$clickday.addClass('selected-cell-font');
			// 日付別一覧の検索
			listPerDate.search(e, $clickday.get(0).innerText);
		});
	},
	// 検索します
	search: function(e, day) {
		e.preventDefault();
		var searchYear = $('#custom-year').text();
		var searchMonth = ('00' + $('#custom-month').attr('month-key')).slice(-2);
		var searchDay = ('00' + day).slice(-2);

		// 送信します
		$.post('/listPerDate/search', {'searchDay': searchYear + searchMonth + searchDay},
			function(data) {
				// 日付別一覧部を書き換えます
				$('table.allStudyUnitsTable').html(data);
			}, 'html');
		return;
	},
	// 勉強単位データが存在する日付にスタイルを追加します
	addExistDataFlg: function() {
		var $existDataLists = $('.exist-data-lists');
		for(var i = 0; i < $existDataLists.length; i++) {
			$.each($('#calendar').find('.fc-body').find('.js-cell').children('.fc-date'), function() {
				if ($existDataLists.get(i).value == $(this).text()) {
					$(this).addClass('exist-data');
				}	
			});
		}
	},
	// 勉強単位データが存在する日付を更新します
	updateExistDataList: function() {
		var searchYear = $('#custom-year').text();
//		var movedMonth = +$('#custom-month').attr('month-key') + monthDiff;
		var searchMonth = ('00' + $('#custom-month').attr('month-key')).slice(-2);

		// 送信します
		$.post('/listPerDate/update', {'movedMonth': searchYear + searchMonth + '00'},
			function(data) {
				// 日付別一覧部を書き換えます
				$('#existDataArea').html(data);
			}, 'html');
		return;
	}
});
var codropsEvents = {};
var showCalendar = function() {	
	var transEndEventNames = {
			'WebkitTransition' : 'webkitTransitionEnd',
			'MozTransition' : 'transitionend',
			'OTransition' : 'oTransitionEnd',
			'msTransition' : 'MSTransitionEnd',
			'transition' : 'transitionend'
		},
		transEndEventName = transEndEventNames[ Modernizr.prefixed( 'transition' ) ],
		$wrapper = $( '#custom-inner' ),
		$calendar = $( '#calendar' ),
		cal = $calendar.calendario( {
			onDayClick : function( $el, $contentEl, dateProperties ) {
				if( $contentEl.length > 0 ) {
					showEvents( $contentEl, dateProperties );
				}
			},
			caldata : codropsEvents,
			displayWeekAbbr : true
		} ),
		$month = $( '#custom-month' ).html( cal.getMonthName() ),
		$year = $( '#custom-year' ).html( cal.getYear() );
	
		$month.attr('month-key', cal.getMonth());
		listPerDate.addExistDataFlg();

	$( '#custom-next' ).on( 'click', function() {
		cal.gotoNextMonth( updateMonthYear );
		listPerDate.addClickEvent();
		listPerDate.updateExistDataList();
		setTimeout(function() {listPerDate.addExistDataFlg() }, 3000);
	} );
	$( '#custom-prev' ).on( 'click', function() {
		cal.gotoPreviousMonth( updateMonthYear );
		listPerDate.addClickEvent();
		listPerDate.updateExistDataList();
		setTimeout(function() {listPerDate.addExistDataFlg() }, 3000);
	} );

	function updateMonthYear() {				
		$month.html( cal.getMonthName() );
		$year.html( cal.getYear() );
		$month.attr('month-key', cal.getMonth());
	}

	// just an example..
	function showEvents( $contentEl, dateProperties ) {
		hideEvents();		
		var $events = $( '<div id="custom-content-reveal" class="custom-content-reveal"><h4>Events for ' + dateProperties.monthname + ' ' + dateProperties.day + ', ' + dateProperties.year + '</h4></div>' ),
			$close = $( '<span class="custom-content-close"></span>' ).on( 'click', hideEvents );
		$events.append( $contentEl.html() , $close ).insertAfter( $wrapper );
		setTimeout( function() {
			$events.css( 'top', '0%' );
		}, 25 );
	}

	function hideEvents() {
		var $events = $( '#custom-content-reveal' );
		if( $events.length > 0 ) {
			$events.css( 'top', '100%' );
			Modernizr.csstransitions ? $events.on( transEndEventName, function() { $( this ).remove(); } ) : $events.remove();
		}
	}
};

$(document).ready(function() {
	// windowのLoad終了後イベント
	$(window).load(function(){
		// カレンダー表示
		showCalendar();
		// カレンダークリックイベント追加
		listPerDate.addClickEvent();
	});
});
