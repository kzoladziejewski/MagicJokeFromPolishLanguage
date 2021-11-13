import React from 'react'
// import { Link } from "react-router-dom";

const Home = () => {
    const [res, setRes] = React.useState([]);

    const setData = async () => {
        const response = await fetchStatus();
        console.log(response)
        setRes(response)
    }
    React.useEffect(() => {

        setData()
    }, [])

    const fetchStatus = () => {
        return fetch('http://127.0.0.1:8080/joke')
            .then(response => response.json())
    }

const vote = (vote) => {

    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: res.id, vote:vote})
    };
    console.log("AAAAAAAAAAAAAAAAA");
    fetch('http://127.0.0.1:8080/static', requestOptions)
    .then(response => response.json());

}

    const ButtonMenda = {
        
    }

    const buttonStyle_good = {
        ...ButtonMenda,
        color: "green",
        
    }

    const buttonStyle_bad = {
        ...ButtonMenda,

        color: "red",
    }

        return ( <div className = "QA" > 
        <center>
        <h1>{(res.joke_question)} </h1>
        <h2>{(res.joke_answer)}</h2>
        {/* <button onClick=vote(1)>Dobrze</button> */}
        {/* <button onClick=vote(-1)>Zle</button> */}
        <button style={buttonStyle_good} onClick={() => vote(1)}> W sumie śmieszne </button>
        <button style={buttonStyle_bad} onClick={() => vote(1)}> Żałosne </button></center>
        {/* <ButtonMailto label="Write me an E-Mail" mailto="mailto:no-reply@example.com" /> */}
        <h4> Jeśli ten żart jest niepoprawny gramatycznie: </h4>
        <a href="mailto:magicpolishjokes_help@kacpur.pl?subject=Zgłoszenie%20złego%20żartu!&body=%20">kliknuj tutaj </a>
        <h4>Albo napisz: magicpolishjokes_help@kacpur.pl </h4>

        <h4>API do wykorzystania:</h4>
        <h4>GET</h4>
        <h4>/joke - pobranie żartu</h4>
        
        </div> )

}


export default Home