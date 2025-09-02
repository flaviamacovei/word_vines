import React from 'react';
import DataDisplay from './components/DataDisplay';
import useFetchData from './hooks/useFetchData';

const App: React.FC = () => {
    const { data, loading, error } = useFetchData('https://api.openbrewerydb.org/v1/breweries');
    console.log(data);
    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error}</div>;

    return (
        <div>
            <h1>Synonyms</h1>
            <DataDisplay data={data} />
        </div>
    );
};

export default App;