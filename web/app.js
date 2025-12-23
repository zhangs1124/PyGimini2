const parameters = {
    "領域": ["教育", "醫療", "金融", "科技", "環保", "人工智能", "娛樂", "運動", "藝術", "旅遊", "飲食", "時尚"],
    "結構": ["開放式", "邏輯樹狀", "流程圖解", "模組化", "互動式", "分散式", "階層式", "網狀", "循環式", "自適應"],
    "複雜度": ["基礎概念", "進階應用", "策略分析", "創新突破", "跨域整合", "前瞻研究", "實驗性質", "理論驗證", "市場驗證", "用戶體驗"],
    "教育階段": ["小學", "中學", "大學", "研究所", "職業培訓", "終身學習", "幼兒教育", "成人教育", "專業認證", "技職教育"],
    "應用場景": ["遠距教學", "智慧醫療", "金融科技", "智慧城市", "永續發展", "元宇宙", "智慧家庭", "智慧交通", "智慧零售", "智慧工廠"],
    "技術方法": ["深度學習", "機器學習", "自然語言處理", "電腦視覺", "強化學習", "聯邦學習", "區塊鏈", "物聯網", "擴增實境", "虛擬實境"]
};

function getRandom(key) {
    const list = parameters[key];
    return list[Math.floor(Math.random() * list.length)];
}

function generateQuestion() {
    const domain = getRandom("領域");
    let template = "";

    if (domain === "教育" || true) { // 為了演示，我們使用一個通用模板或隨機組合
        template = `在${getRandom("應用場景")}的背景下，如何運用${getRandom("技術方法")}來實現${getRandom("結構")}的系統，並達到${getRandom("複雜度")}的目標？`;
    }
    return template;
}

$(document).ready(function () {
    // 嘗試從本地讀取以前存過的 API Key (僅作方便使用)
    const savedKey = localStorage.getItem('groq_api_key');
    if (savedKey) $('#api-key').val(savedKey);

    $('#btn-generate').click(async function () {
        const apiKey = $('#api-key').val().trim();
        const customText = $('#custom-question').val().trim();

        if (!apiKey) {
            alert("請輸入 API Key！");
            return;
        }

        // 儲存 Key
        localStorage.setItem('groq_api_key', apiKey);

        // UI 狀態切換
        $('#loader').show();
        $('#btn-generate').prop('disabled', true).text('分析中...');
        $('#status-bar').text('正在處理...');

        // 邏輯平衡：優先使用手打文字，否則自動生成
        let question = "";
        if (customText) {
            question = customText;
            $('#status-bar').text('使用自定義詢問內容...');
        } else {
            question = generateQuestion();
            $('#status-bar').text('正在生成隨機題目...');
        }
        $('#generated-question').text(question);
        $('#question-section').fadeIn();

        const prompt = question + " 請給我10個簡單的搜尋問題，格式如下：1. 第一個問題 2. 第二個問題... 請直接列出問題，不要有其他說明文字。";

        try {
            $('#status-bar').text('正在呼叫 Groq API...');

            const response = await fetch("https://api.groq.com/openai/v1/chat/completions", {
                method: "POST",
                headers: {
                    "Authorization": `Bearer ${apiKey}`,
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    model: "llama-3.3-70b-versatile",
                    messages: [{ role: "user", content: prompt }],
                    temperature: 0.7
                })
            });

            if (!response.ok) throw new Error(`API 錯誤: ${response.status}`);

            const data = await response.json();
            const content = data.choices[0].message.content;

            // 解析結果 (假設格式為 1. xxx 2. xxx)
            const lines = content.split('\n').filter(l => l.trim().match(/^\d+\./));

            $('#queries-list').empty();
            if (lines.length === 0) {
                // 如果格式不如預期，嘗試簡單分割
                content.split('\n').forEach(line => {
                    if (line.trim()) appendListItem(line.trim());
                });
            } else {
                lines.forEach(line => {
                    const text = line.replace(/^\d+\.\s*/, '');
                    appendListItem(text);
                });
            }

            $('#status-bar').text('完成！點擊項目可直接在 Bing 搜尋。');

        } catch (error) {
            console.error(error);
            $('#status-bar').text('發生錯誤: ' + error.message);
            alert("呼叫 API 失敗，請確認 Key 是否正確或網路通暢。");
        } finally {
            $('#loader').hide();
            $('#btn-generate').prop('disabled', false).text('再次生成並分析');
        }
    });

    function appendListItem(text) {
        const escapedText = $('<div>').text(text).html();
        const $li = $(`<li>${escapedText}</li>`);
        $li.click(function () {
            window.open(`https://www.bing.com/search?q=${encodeURIComponent(text)}`, '_blank');
        });
        $('#queries-list').append($li);
    }
});
