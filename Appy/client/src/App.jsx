import { useState, useEffect } from 'react'
import './App.css'
import axios from "axios"

function App() {
  const [count, setCount] = useState(0)
  const [array, setArray] = useState([])

  const fetchAPI = async() => {
    const response = await axios.get("http://127.0.0.1:8080/api/users");
    console.log(response.data.users);
    setArray(response.data.users);
  }

  useEffect(() => {
    fetchAPI();
  }, [])

  return (
    <>
      <div>
        <p>
          {
            array.map((item, index) => {
              return (
                <li key={index}>
                  {item.name}
                </li>
              )
            })
          }
        </p>
      </div>
    </>
  )
}

export default App
