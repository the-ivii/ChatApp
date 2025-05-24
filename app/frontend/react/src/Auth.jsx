import axios from 'axios';

const Auth = (props) => {
    const onSubmit = (e) => {
        e.preventDefault();
        const {value}= e.target[0];
        axios.post('http://localhost:3001/authenticate', {username: value})
        props.onAuth({username: value, secret: value});
    }
    return(
        <div className='background'>
            <form onSubmit={onSubmit} className='form'>
                <div className='welcome'>
                    WELCOME! 
                </div>
                <div className='heading'>
                    Set a username to get started
                </div>
                <div className='auth'>
                    <div className='text'>Username</div>
                    <input className='input' placeholder='Username' type='text' name='username'/>
                    <button className='authButton' type='submit'>Enter Chat Room</button>
                </div>
            </form>
        </div>
    )
}

export default Auth;