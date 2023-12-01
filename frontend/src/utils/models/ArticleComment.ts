import User from "./User.ts";

export default interface ArticleComment {
    id: number;
    comment_text: string;
    created_date: Date;
    updated_date?: Date|null;
    parent_comment?: number|null;
    user: number | User;

    replies: ArticleComment[];
};