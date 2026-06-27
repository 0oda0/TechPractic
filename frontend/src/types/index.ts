export interface Document {
  id: string;
  file_name: string;
  upload_date: string;
  status: string;
  total_pages: number;
}

export interface SearchResult {
  chunk_id: string;
  file_name: string;
  page: number;
  text: string;
  score: number;
}

export interface SearchResponse {
  results: SearchResult[];
  total: number;
  took: number;
}