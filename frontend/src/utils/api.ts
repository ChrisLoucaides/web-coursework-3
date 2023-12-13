import ArticleComment from "./models/ArticleComment.ts";
import User from './models/User.ts'
import Article from "./models/Article.ts";
import Cookies from "js-cookie";

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
        const result = await fetch(`${this.url}users/current`, { credentials: 'include' });
        return await result.json() as User;
    }

    static fetchArticles = async (): Promise<Article[]> => {
        const result = await fetch(`${this.url}articles`, { credentials: 'include' });
        return await result.json() as Article[];
    }

    static updatePreferences = async (json: any): Promise<number> => { //TODO WEB-9: change to updateUser and change url path
        var csrftoken = Cookies.get('csrftoken')
        if (csrftoken==null) {
            csrftoken = 'BLAHBLAH'
        }
        const header = new Headers()
        header.append('X-CSRFToken', csrftoken)
        header.append('content-type', 'application/json')
        const response = await fetch(`${this.url}users/update_user/`, {
            method: 'PATCH',
            headers: header,
            body: json,
            credentials: 'include',
        });
        console.log(response)
        console.log(response.json())

        return response.status
        // return await result.json() as Article[];
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