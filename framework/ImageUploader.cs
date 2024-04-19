using UnityEngine;
using UnityEngine.Networking;
using System.Collections;
using SFB; // StandaloneFileBrowser namespace
using System.IO;

public class ImageUploader : MonoBehaviour
{
    public string uploadURL = "http://localhost:5000/upload"; // Flask服务的URL

    // 调用这个方法来选择并上传图片
    public void UploadImage()
    {
        var paths = StandaloneFileBrowser.OpenFilePanel("Select Image", "", "png", false);
        if (paths.Length > 0)
        {
            StartCoroutine(UploadCoroutine(paths[0]));
        }
    }

    IEnumerator UploadCoroutine(string imagePath)
    {
        byte[] imageBytes = File.ReadAllBytes(imagePath);
        WWWForm form = new WWWForm();
        form.AddBinaryData("image", imageBytes, Path.GetFileName(imagePath), "image/png");

        using (UnityWebRequest www = UnityWebRequest.Post(uploadURL, form))
        {
            yield return www.SendWebRequest();

            if (www.result != UnityWebRequest.Result.Success)
            {
                Debug.LogError(www.error);
            }
            else
            {
                Debug.Log("Image uploaded successfully!");
            }
        }
    }
}
