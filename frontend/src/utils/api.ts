import ArticleComment from "./models/ArticleComment.ts";
import User from './models/User.ts'

class API {

    private static url: string = "http://127.0.0.1:8000/api/";

    /**
     * Fetches a list of comments and replies for a specified article id
     * @param articleId The id of the article
    */
    static fetchCommentsForArticle = async (articleId: number): Promise<ArticleComment[]> => {
        const result = await fetch(`${this.url}article/${articleId}/comments`);
        return await result.json() as ArticleComment[];
    }

    static fetchUser = async (): Promise<User> => {
        const result = await fetch(`http://127.0.0.1:8000/current_user`, {credentials:'same-origin'});
        return await result.json() as User;
    }

    /**
     * Creates a new comment and returns the created ArticleComment
     * @param articleId The id of the article to post to
     * @param comment The new comment model
     */
    static postComment = async (articleId: number, comment: ArticleComment): Promise<ArticleComment> => {
        const result = await fetch(`${this.url}article/${articleId}/comments`, {
            method: 'POST',
            body: JSON.stringify(comment)
        });
        return await result.json() as ArticleComment;
    }
}

export default API;