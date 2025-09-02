export interface DataItem {
    id: number;
    name: string;
    value: number;
}

export interface FetchDataResponse {
    data: DataItem[];
    message?: string;
}

export interface FetchDataError {
    message: string;
}