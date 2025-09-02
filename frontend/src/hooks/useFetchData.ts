import { useEffect, useState } from 'react';

const useFetchData = (url: string) => {
    const [data, setData] = useState<any>(null);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch(url);
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const result = await response.json();
                setData(result);
                setData({"centre":"test","synonyms":[{"abc": [-1, 1]}, {"def": [-0.5, 0.5]}, {"ghi": [0.7, 0.9  ]}]});
            } catch (error) {
                if (error instanceof Error) {
                    setError(error.message);
                } else {
                    setError(String(error));
                }
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [url]);
    
    return { data, loading, error };
};

export default useFetchData;