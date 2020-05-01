let clicked_element_position = {};
let temp_section_text = [];
let temp_section_title_val = [];
let temp_section_article_val = [];


$(document).ready(function () {
    initialize_event_handler();
});

function initialize_event_handler() {
    //イベントハンドラ
    add_section();
    delete_section();
    get_clicked_element_position('input[name="delete_section_button"]');
    get_clicked_element_position('input[name="preview_section_button"]');
    get_clicked_element_position('input[name="edit_section_button"]');
    get_clicked_element_position('textarea[name="guide_section_article"]');
    add_youtube_tag();
    add_link_tag();
    add_bold_tag();
    add_italic_tag();
    add_bolditalic_tag();
    preview_section();
    edit_section();
    preview_guide();
    post_guide();
}

/*
 *セクションごとのイベントハンドラ
 */

//sectionの追加ボタン
function add_section() {
    $(document).on('click', 'input[name="add_section_button"]', function () {
        let additional_html =
            '<div class="guide_section" name="guide_section">' +
            '<div class="guide_section_title">' +
            '<input type="text" name="guide_section_title" size="60" value="セクションのタイトル">' +
            '</div>' +
            '<div class="guide_section_article">' +
            '<textarea name="guide_section_article" cols ="100" rows = "30" >' +
            '新しいセクションです。ここに記事を書いていきましょう!' +
            '</textarea>' +
            '</div>' +
            '<div class="guide_section_button_area" name="guide_section_button_area">' +
            '<input type="button" name="delete_section_button" value="セクション削除">' +
            ' <input type="button" name="preview_section_button" value="簡易プレビュー">' +
            '</div>' +
            '</div>';
        $('div[name="guide_editor"]').append(additional_html);

    });
}

function delete_section() {
    $(document).on('click', 'input[name="delete_section_button"]', function () {
        let isDelete = window.confirm("本当に段落を削除してよろしいですか");
        let index = $('[name="guide_section"]').index(this.parentElement.parentElement);
        if (isDelete) {
            $('div[name="guide_section"]').eq(index).remove();
        }
    });
}


//編集モードへの切替ボタン(section)
function preview_section() {
    $(document).on('click', 'input[name="preview_section_button"]', function () {
        let index = $('[name="guide_section"]').index(this.parentElement.parentElement);
        let $section = $('div[name="guide_section"]').eq(index);
        console.log("preview_index: " + index);
        //セクションの内容を一時保存
        temp_section_text[index] = $section.html();
        temp_section_title_val[index] = $section.find('input[name="guide_section_title"]');
        temp_section_article_val[index] = $section.find('textarea[name="guide_section_article"]');
        let html_code = section_convert_to_html($section);
        console.log(html_code);
        $('div[name="guide_section"]').eq(index).html(html_code["contents"] + html_code["edit_button"]);
    });
}

//編集モードへの切替ボタン
function edit_section() {
    $(document).on('click', 'input[name="edit_section_button"]', function () {
        let index = $('div[name="guide_section"]').index(this.parentElement.parentElement);
        let $section = $('div[name="guide_section"]').eq(index);
        console.log("editindex: " + index);
        $section.html(temp_section_text[index]);
        $section.find('input[name="guide_section_title"]').val(temp_section_title_val[index].val());
        $section.find('textarea[name="guide_section_article"]').val(temp_section_article_val[index].val());
    });
}

//どのボタンが押されたのかの確認。
function get_clicked_element_position(selector) {
    $(document).on("click", selector, function () {
        clicked_element_position[selector] = $(selector).index(this);
        console.log("clicked_" + selector + ":" + clicked_element_position[selector]);
    });
}


//footer部のイベントハンドラ
//selection()については、https://madapaja.github.io/jquery.selection/ja_jp.html　参照
//youtubeタグ追加
function add_youtube_tag() {
    $('input[name="add_youtube_button"]').on("click", function () {
        let youtube_id = prompt("貼り付けたいyoutube動画のIDを入力してください。", "");
        $('textarea[name="guide_section_article"]').eq(clicked_element_position['textarea[name="guide_section_article"]']).selection('replace', {text: '[youtube=\(' + youtube_id + '\)]'});
    });
}


function add_link_tag() {
    $('input[name="add_link_button"]').on("click", function () {
        let link_address = prompt("貼り付けたいリンクのアドレスを入力してください。", "");
        if (link_address == null || link_address == "") {
            return;
        }
        let link_word = prompt("貼り付けたいリンクの言葉を入力してください。", "");
        if (link_word == null) {
            return;
        }
        console.log(clicked_element_position['textarea[name="guide_section_article"]']);
        $('textarea[name="guide_section_article"]').eq(clicked_element_position['textarea[name="guide_section_article"]']).selection('replace', {text: '[' + link_word + '](' + link_address + ')'});
    })
}

function add_bold_tag() {
    $('input[name="add_bold_button"]').on("click", function () {
        let selected_word = $('textarea[name="guide_section_article"]').eq(clicked_element_position['textarea[name="guide_section_article"]']).selection();
        $('textarea[name="guide_section_article"]').eq(clicked_element_position['textarea[name="guide_section_article"]']).selection('replace', {text: '*' + selected_word + '*'});
    })
}

function add_italic_tag() {
    $('input[name="add_italic_button"]').on("click", function () {
        let selected_word = $('textarea[name="guide_section_article"]').eq(clicked_element_position['textarea[name="guide_section_article"]']).selection();
        $('textarea[name="guide_section_article"]').eq(clicked_element_position['textarea[name="guide_section_article"]']).selection('replace', {text: '**' + selected_word + '**'});
    })
}

function add_bolditalic_tag() {
    $('input[name="add_bolditalic_button"]').on("click", function () {
        let selected_word = $('textarea[name="guide_section_article"]').eq(clicked_element_position['textarea[name="guide_section_article"]']).selection();
        $('textarea[name="guide_section_article"]').eq(clicked_element_position['textarea[name="guide_section_article"]']).selection('replace', {text: '***' + selected_word + '***'});
    })
}

//プレビューボタン押下時のメソッド
function preview_guide() {
    $(document).on('click', 'input[name="preview_button"]', function () {
        //ガイドタイトルが空欄の場合の処理
        if ($('input[name = "guide_title"]').eq(0).val() == "") {
            alert("ガイドタイトルには必ずタイトルを入力してください")
            return;
        }
        let edit_buttons = document.getElementsByName("edit_section_button");

        if (edit_buttons[0] != undefined) {
            let num_of_edit_buttons = edit_buttons.length;

            for (let i = 0; i < num_of_edit_buttons; i++) {
                console.log("edit_buttons length : " + edit_buttons.length);
                edit_buttons[0].click();
            }
        }

        let guide_html = guide_convert_to_html();

        create_preview_window(guide_html);
    })
}

function post_guide() {
    $(document).on('click', 'input[name="post_guide_button"]', function () {
        //ガイドタイトルが空欄の場合の処理
        if ($('input[name = "guide_title"]').eq(0).val() == "") {
            alert("ガイドタイトルには必ずタイトルを入力してください")
            return;
        }
        let is_postable = window.confirm("本当にこの内容で投稿してよろしいですか？");
        if (is_postable == false) {
            return;
        }

        let edit_buttons = document.getElementsByName("edit_section_button");
        console.log("edit_buttons length : " + edit_buttons.length);
        if (edit_buttons[0] != undefined) {
              let num_of_edit_buttons = edit_buttons.length;
            for (let i = 0; i < num_of_edit_buttons ;i++) {
                edit_buttons[0].click();
            }
        }

        document.guide_form.target = "_self";
        document.guide_form.method = "post";
        document.guide_form.action = "";
        document.guide_form.submit();

    })
}


//フォームの中に入っているsectionをＨＴＭＬにコンバートするためのメソッド
function section_convert_to_html($section) {
    let section_title_val = $section.find('input[name="guide_section_title"]').val();
    let section_article_val = $section.find('textarea[name="guide_section_article"]').val();

    console.log(section_title_val);
    console.log(section_article_val);
    //マークダウン
    //改行を体感的に行うための下処理


    //マークダウンの改行設定
    marked.setOptions({breaks: true});
    section_title_val = marked(section_title_val);
    section_article_val = marked(section_article_val);


    //カスタムタグ追加
    //youtubeタグ
    section_article_val = section_article_val.replace(/\[youtube=\((.*)\)\]/g, '<iframe width="560" height="315" src="https://www.youtube.com/embed/$1" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>');


    let html_code = {};
    html_code["contents"] = '<div class=\"guide_section_title_preview\">' +
        section_title_val +
        '</div>' +
        '<div class=\"guide_section_article_preview\">' +
        section_article_val +
        '</div>';
    html_code["edit_button"] =
        '<div class=\"guide_section_button_area\" name=\"guide_section_button_area\">' +
        ' <input type=\"button\" name=\"edit_section_button\" value=\"編集モード\">' +
        '</div>';

    return html_code;
}


//ガイド全体をhtmlにコンバート
function guide_convert_to_html() {
    let section_length = $('div[name="guide_section"]').length;
    let guide_html = {};
    guide_html["guide_section"] = [];
    console.log("aaa:" + ($('div[name="guide_section"]').eq(0)));
    for (let i = 0; i < section_length; i++) {
        guide_html["guide_section"][i] = section_convert_to_html($('div[name="guide_section"]').eq(i));
        console.log(guide_html["guide_section"][i]);
    }
    guide_html["guide_title"] = $('input[name="guide_title"]').eq(0).val();
    guide_html["guide_character"] = $('select[name="guide_character"] option:selected').eq(0).val();
    guide_html["guide_category"] = $('select[name="guide_category"] option:selected').eq(0).val();

    console.log("section_length :" + section_length);
    console.log("guide_title :" + guide_html["guide_title"]);
    console.log("guide_category:" + guide_html["guide_character"]);
    console.log("guide_category:" + guide_html["guide_category"]);

    return guide_html;

}


//プレビューウィンドウ作成メソッド
function create_preview_window(guide_html) {
    document.guide_form.target = "_blank";
    document.guide_form.method = "post";
    document.guide_form.action = "/guide/create/preview/";
    document.guide_form.submit();
}



