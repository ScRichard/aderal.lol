
import axios from 'axios';
import Messages from "./messages/Messages";


class Handler {

    static async post_response(url : string, data : any){
        try {
            return (await axios.post(url, data)).data;
        } catch (error) {
            return {
                Error: Messages.ERROR_MESSAGE,
                CATCH: error
            }
        }
        
    }

    static async handleRegister(username : string, token : string) {
        return this.post_response('http://127.0.0.1:5000/register', {
            "username": username,
            "token": token
        })
    }
    static async handleLogin(token : string) {
        return this.post_response('http://127.0.0.1:5000/login', {
            "token": token
        })
    }
}

function LoginPanel() {
    return (
        <div className='flex flex-col p-8 bg-slate-500 gap-6 w-auto'>
            <h1 className='text-zinc-200 text-lg underline'>Welcome to Aderal.lol</h1>
        </div>
    )
};

export default { Handler, LoginPanel };