// ============================================================
//  影片連結（由 site_writeback.py 自動回寫，也可以手動改）
//  youtube ：影片 ID 或網址      short  ：直式重點版（Shorts）ID
//  duration：片長 "6:35"          sections：各小節開始秒數（數量＝小節數），null 用 content.js 預估
//  noVoice ：無旁白版 ID          mp4    ：自架 MP4（沒有 YouTube 時才用）
// ============================================================

window.SERIES_PLAYLIST = ""; // 系列播放清單網址（公開或不公開後才填）
window.SERIES_TRAILER = "";  // 系列前導片 ID（延續型系列）

window.VIDEO_LINKS = {
  u01: { youtube: "fQMXteBpl-s", mp4: "", duration: "12:58", sections: [0, 13, 46.7, 138.1, 301.1, 399.9, 510.2, 673.1], noVoice: "", short: "" },
  u02: { youtube: "ClIb4KlPR8I", mp4: "", duration: "12:34", sections: [0, 13, 53.6, 144.1, 245.5, 389, 500.1, 609.4], noVoice: "", short: "" },
  u03: { youtube: "TGmNwKHrCRg", mp4: "", duration: "13:18", sections: [0, 13, 58.2, 167.9, 266.3, 387.3, 510.2, 615.2], noVoice: "", short: "" },
  u04: { youtube: "tKUopTb2wI8", mp4: "", duration: "13:25", sections: [0, 13, 53.9, 165.7, 254.4, 392.4, 555.6, 676.9], noVoice: "", short: "" },
  u05: { youtube: "", mp4: "", duration: "", sections: null, noVoice: "", short: "" },
  u06: { youtube: "", mp4: "", duration: "", sections: null, noVoice: "", short: "" },
  u07: { youtube: "", mp4: "", duration: "", sections: null, noVoice: "", short: "" },
  u08: { youtube: "", mp4: "", duration: "", sections: null, noVoice: "", short: "" },
  u09: { youtube: "", mp4: "", duration: "", sections: null, noVoice: "", short: "" },
  u10: { youtube: "", mp4: "", duration: "", sections: null, noVoice: "", short: "" },
  u11: { youtube: "", mp4: "", duration: "", sections: null, noVoice: "", short: "" },
  u12: { youtube: "", mp4: "", duration: "", sections: null, noVoice: "", short: "" }
};
