import Suggestion from "../models/Suggestion";

export default interface NewsArticle {
  title: string;
  url: string;
  abstract: string;
  suggestions: Suggestion[];
}
