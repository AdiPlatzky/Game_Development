
using UnityEngine;

[RequireComponent(typeof(Camera))]
public class ResponsiveCamera2D : MonoBehaviour
{
    [Header("Follow Target")]
    [SerializeField] private Transform playerTarget;

    [Header("Camera Zoom")]
    [SerializeField]
    private float halfWorldSizeOnShortSide = 5f;

    private Camera gameCamera;

    private void Awake()
    {
        gameCamera = GetComponent<Camera>();
        gameCamera.orthographic = true;
    }

    private void LateUpdate()
    {
        FollowPlayer();
        AdjustCameraSize();
    }

    private void FollowPlayer()
    {
        if (playerTarget == null)
            return;

        Vector3 cameraPosition = transform.position;

        cameraPosition.x = playerTarget.position.x;
        cameraPosition.y = playerTarget.position.y;

        transform.position = cameraPosition;
    }

    private void AdjustCameraSize()
    {
        float shortSide = Mathf.Min(
            Screen.width,
            Screen.height
        );

        if (shortSide <= 0f)
            return;

        gameCamera.orthographicSize =
            halfWorldSizeOnShortSide *
            Screen.height / shortSide;
    }
}
