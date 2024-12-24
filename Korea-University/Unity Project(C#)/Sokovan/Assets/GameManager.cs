using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GameManager : MonoBehaviour
{
    public ItemBox[] ItemBoxes;

    public bool isGameOver;

    public GameObject winUI;
    // Start is called before the first frame update
    void Start()
    {
        isGameOver = false;
        
    }

    // Update is called once per frame
    void Update()
    {

        if(Input.GetKeyDown(KeyCode.Space)) {
            Application.LoadLevel(0);
        }
        if(isGameOver == true) {
            return;
        }
        int count = 0;
        for(int i = 0; i < 3; i++) {
            if(ItemBoxes[i].isOveraped == true) {
                count++;
            }
        }

        if(count >= 3) {
            isGameOver = true;
            Debug.Log("게임 승리");
            winUI.SetActive(true);
        }
    }
}
