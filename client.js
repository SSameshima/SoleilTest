const axios = require('axios');

async function testLocationData() {
    try {
        // 基本的な接続テスト
        const response = await axios.get('http://localhost:5000/api/test');
        console.log('サーバーからの応答:', response.data);

        // buildingAの位置と人数を保存
        const locationResponse = await axios.post('http://localhost:5000/api/location', {
            place_pos: 'buildingA',
            count_person: '2',
            timestamp: new Date().toISOString()
        });
        console.log('位置データの保存結果:', locationResponse.data);

        // buildingBの位置と人数を保存
        const location2Response = await axios.post('http://localhost:5000/api/location', {
            place_pos: 'buildingB',
            count_person: '5',
            timestamp: new Date().toISOString()
        });
        console.log('2つ目の位置データの保存結果:', location2Response.data);

        // 全ての位置データを取得
        const allLocationsResponse = await axios.get('http://localhost:5000/api/location');
        console.log('保存されている全位置データ:', JSON.stringify(allLocationsResponse.data, null, 2));

    } catch (error) {
        console.error('エラーが発生しました:', error.message);
    }
}

testLocationData(); 