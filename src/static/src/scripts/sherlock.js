$(document).ready(() =>
{
    var store = new Store();

    var article_uploaded = new ArticleUploaded("#article-uploaded", store);
    article_uploaded.fade_body_in();
    article_uploaded.on("update", () =>
    {
        article.fade_body_out().then(() =>
        {
            article.refresh();
            article.refresh_table(0, true);
            article.fade_body_in();
        });
    });

    var upload = new FileUpload("#btn-upload", "text/csv", (name, modified, size, data)  =>
    {
        store.insert_file(name, modified, size, data);
        article_uploaded.refresh();
    });

    var article = new ArticleSherlock("#article-sherlock", store);
    article.refresh();
    article.fade_body_in();

});