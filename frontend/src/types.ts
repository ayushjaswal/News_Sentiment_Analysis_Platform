
export interface ExpectedData {
    "frame_model": string
    "sens_and_opin": string
    "pol_model": string

}

export interface NewsData {
    articles: string[];
    predictions: ExpectedData[];
    summaries: string[];
  }