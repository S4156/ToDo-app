'use strict';

let player;

/**
 * 埋め込み動画を作成
 */
    function onYouTubeIframeAPIReady() {
      const videoId = window.videoIdFromTemplate;
      player = new YT.Player('player', {
        videoId: videoId,
        PlayerVars:{
          rel: 0
        },
        events: {
          'onStateChange': onPlayerStateChange
        }
      });
    }

/**
 * 動画の終了を検知したら、タスクページにリダイレクト
 */
    function onPlayerStateChange(event) {
      if (event.data == YT.PlayerState.ENDED) {
        // 終了したらリダイレクト
        window.location.href = '/';
      }
    }
    