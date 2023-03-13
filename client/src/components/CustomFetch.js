/* eslint-disable */
  // eslint-disable-next-line
  async function CustomFetch(url, init_object) {
    let res = null
    let data = null
    try {
        res = await fetch(url, init_object)
    }
    catch {
        throw new Error("Network conndection failed")
    }
    try {
        data = await res.json()
    }
    catch {
        throw new Error("Response body was not json")
    }

    if(res.ok) {
        return data
    }
    else {
        throw new Error(data.message)
    }
}

export default CustomFetch