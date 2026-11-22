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
  u05: { youtube: "xcZwbk519fI", mp4: "", duration: "13:53", sections: [0, 13, 54.5, 158.7, 279.1, 374.1, 564.8, 713.1], noVoice: "", short: "" },
  u06: { youtube: "1krAsIMBcak", mp4: "", duration: "13:56", sections: [0, 13, 46.7, 121.3, 214.7, 312.8, 497.1, 689.3], noVoice: "", short: "" },
  u07: { youtube: "2AIzmCrIoS8", mp4: "", duration: "13:37", sections: [0, 13, 51.3, 163.2, 261.2, 404.5, 533.5, 692.8], noVoice: "", short: "" },
  u08: { youtube: "9QWOwqh3774", mp4: "", duration: "13:45", sections: [0, 13, 46.6, 135.8, 292.1, 461.4, 562.1, 663], noVoice: "", short: "" },
  u09: { youtube: "22jfnF_69Wg", mp4: "", duration: "13:02", sections: [0, 13, 47.2, 161, 311, 446.3, 550.5, 667], noVoice: "", short: "" },
  u10: { youtube: "ISx2pgW8pjo", mp4: "", duration: "13:06", sections: [0, 13, 56.5, 158.7, 256.2, 382.9, 517.8, 644.4], noVoice: "", short: "" },
  u11: { youtube: "KcThKQXkrZo", mp4: "", duration: "13:57", sections: [0, 13, 50.6, 159.9, 271.9, 396.1, 599.7, 713.6], noVoice: "", short: "" },
  u12: { youtube: "UtBFzzJfXBs", mp4: "", duration: "13:33", sections: [0, 13, 47.4, 145.7, 247.5, 363.4, 459, 557.8, 720.9], noVoice: "", short: "" }
};
