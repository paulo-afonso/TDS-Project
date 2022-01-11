import React from 'react';
import Navbar from '../components/Navbar';
import '../styles/index.css'

const Index = () => {
    const [boards, setBoards] = React.useState([]);
    const [boardId, setBoardId] = React.useState([]);

    React.useEffect(() => {
        getBoards();
    }, []);

    async function getBoards() {
        await fetch('http://127.0.0.1:8000/boards/')
            .then(resp => resp.json())
            .then(data => {
                console.log(data);
                if(data) setBoards(data);
            })
    }

    return (
        <div id='index-page'>
            <Navbar />
            {/* <form> */}
                <div className='boards'>
                    <h1>Seus Quadros</h1>
                    <div className='boards-container'>
                    {boards.map(board => (
                            <button key={board.id} onClick={() => {
                                setBoardId(board.id)
                            }}>{board.name}</button>
                            ))}
                            </div>
                </div>
            {/* </form> */}
            {boardId ? <p>{boardId}</p> : ''}
        </div>
    );
}

export default Index;

