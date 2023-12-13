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

    /**
     * Fetches a DTO of the current logged in user
     */
    static fetchUser = async (): Promise<User> => {
        const result = await fetch(`${this.url}users/current`, { credentials: 'include' });
        return await result.json() as User;
    }

    /**
     * Fetches all articles for the current logged in user
     */
    static fetchArticles = async (): Promise<Article[]> => {
        const result = await fetch(`${this.url}articles`, { credentials: 'include' });
        return await result.json() as Article[];
    }

     /**
     * Fetches an article by id
     * @param id The id of the article to retrieve
     */
    static fetchArticle = async (id: number): Promise<Article> => {
        const result = await fetch(`${this.url}articles/${id}`, { credentials: 'include' });
        return await result.json() as Article;
    }

    //TODO: Typescript-ify this (pls make interface and send here :))
    static updatePreferences = async (json): Promise<void> => {
        var csrftoken = Cookies.get('csrftoken')
        if (csrftoken==null) {
            csrftoken = 'BLAHBLAH'
        }
        const header = new Headers()
        header.append('X-CSRFToken', csrftoken)
        header.append('content-type', 'application/json')
        const result = await fetch(`${this.url}users/update_categories/`, {
            method: 'PATCH',
            headers: header,
            body: json,
            credentials: 'include',
        });
        console.log(result)
        console.log(result.json())
        // return await result.json() as Article[];
    }

    /**
     * Creates a new comment and returns the created ArticleComment
     * @param articleId The id of the article to post to
     * @param comment The new comment model
     */
    static postComment = async (articleId: number, comment: ArticleComment): Promise<ArticleComment> => {
        let csrftoken = Cookies.get('csrftoken')
        if (csrftoken==null) {
            csrftoken = 'BLAHBLAH'
        }
        const header = new Headers()
        header.append('X-CSRFToken', csrftoken)
        header.append('content-type', 'application/json')

        const result = await fetch(`${this.url}article/${articleId}/comments/`, {
            method: 'POST',
            headers: header,
            credentials: 'include',
            body: JSON.stringify(comment)
        });
        return await result.json() as ArticleComment;
    }

    /**
     * Updated the text of a comment
     * @param articleId The id of the article
     * @param commentId The id of the comment to update
     * @param comment_text The new text to replace with
     */
    static editComment = async (articleId: number, commentId: number, comment_text: string): Promise<ArticleComment> => {
        let csrftoken = Cookies.get('csrftoken')
        if (csrftoken==null) {
            csrftoken = 'BLAHBLAH'
        }
        const header = new Headers()
        header.append('X-CSRFToken', csrftoken)
        header.append('content-type', 'application/json')

        const result = await fetch(`${this.url}article/${articleId}/comments/${commentId}/`, {
            method: 'PATCH',
            headers: header,
            credentials: 'include',
            body: JSON.stringify({
                comment_text
            })
        });
        return await result.json() as ArticleComment;
    }
}

export default API;