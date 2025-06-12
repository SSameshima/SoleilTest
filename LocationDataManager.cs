using UnityEngine;
using UnityEngine.Networking;
using System.Collections;
using System.Collections.Generic;
using System;
using TMPro;

[System.Serializable]
public class LocationData
{
    public string place_pos;
    public int count_person;
    public string timestamp;
}

[System.Serializable]
public class LocationResponse
{
    public LocationData[] locations;
}

public class LocationDataManager : MonoBehaviour
{
    [SerializeField]
    private string serverIP = "localhost"; // インスペクターで設定可能
    private string ServerBaseUrl => $"http://{serverIP}:5000";

    [SerializeField]
    private TextMeshProUGUI b1,b2,p1,p2;

    
    void Start()
    {
        // 開始時にデータを取得
        StartCoroutine(FetchLocationData());
        
        // 定期的にデータを更新（例：5秒ごと）
        InvokeRepeating("UpdateData", 5f, 5f);
    }

    void UpdateData()
    {
        StartCoroutine(FetchLocationData());
    }

    IEnumerator FetchLocationData()
    {
        using (UnityWebRequest request = UnityWebRequest.Get($"{ServerBaseUrl}/api/location"))
        {
            yield return request.SendWebRequest();

            if (request.result == UnityWebRequest.Result.Success)
            {
                string jsonResponse = request.downloadHandler.text;
                LocationResponse response = JsonUtility.FromJson<LocationResponse>(jsonResponse);

                // 取得したデータを処理
                foreach (LocationData location in response.locations)
                {
                    //Debug.Log($"場所: {location.place_pos}, 人数: {location.count_person}");
                    // ここでUnityのGameObjectを更新するなどの処理を追加
                    if(location.place_pos == "buildingA")
                    {
                        b1.text = location.place_pos;
                        p1.text = location.count_person.ToString();
                    }
                    if (location.place_pos == "buildingB")
                    {
                        b2.text = location.place_pos;
                        p2.text = location.count_person.ToString();
                    }

                    UpdateLocationVisual(location);
                }
            }
            else
            {
                Debug.LogError($"データの取得に失敗: {request.error}");
            }
        }
    }

    // サーバーにデータを送信するメソッド
    public void SendLocationData(string buildingName, int numberOfPeople)
    {
        StartCoroutine(PostLocationData(buildingName, numberOfPeople));
    }

    IEnumerator PostLocationData(string buildingName, int numberOfPeople)
    {
        // POSTするデータを作成
        LocationData data = new LocationData
        {
            place_pos = buildingName,
            count_person = numberOfPeople,
            timestamp = DateTime.UtcNow.ToString("o")
        };

        string jsonData = JsonUtility.ToJson(data);

        using (UnityWebRequest request = UnityWebRequest.PostWwwForm($"{ServerBaseUrl}/api/location", "POST"))
        {
            byte[] bodyRaw = System.Text.Encoding.UTF8.GetBytes(jsonData);
            request.uploadHandler = new UploadHandlerRaw(bodyRaw);
            request.downloadHandler = new DownloadHandlerBuffer();
            request.SetRequestHeader("Content-Type", "application/json");

            yield return request.SendWebRequest();

            if (request.result == UnityWebRequest.Result.Success)
            {
                Debug.Log("データの送信に成功しました");
            }
            else
            {
                Debug.LogError($"データの送信に失敗: {request.error}");
            }
        }
    }

    // 位置情報の視覚的な更新（例：オブジェクトの位置や色を変更）
    private void UpdateLocationVisual(LocationData location)
    {
        // 例：場所の名前を持つGameObjectを探して更新
        GameObject locationObject = GameObject.Find(location.place_pos);
        if (locationObject != null)
        {
            // 人数に応じて色を変更する例
            int count = location.count_person;
            Renderer renderer = locationObject.GetComponent<Renderer>();
            if (renderer != null)
            {
                // 人数に応じて色を変更（例：0人=青、5人以上=赤）
                if (count == 0)
                {
                    renderer.material.color = Color.blue;
                }
                else if (count >= 5)
                {
                    renderer.material.color = Color.red;
                }
                else
                {
                    // 1-4人の場合は青から赤へのグラデーション
                    float t = count / 5f;
                    renderer.material.color = Color.Lerp(Color.blue, Color.red, t);
                }
            }

            // ここに他の視覚的な更新処理を追加
            // 例：テキスト表示、スケール変更など
        }
    }
} 