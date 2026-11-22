
using UnityEngine;
using UnityEngine.InputSystem;

[RequireComponent(typeof(Rigidbody2D))]
public class PlayerMovement2D : MonoBehaviour
{
    [Header("Movement Settings")]
    [SerializeField] private float moveSpeed = 4f;

    [Header("Input Settings")]
    [SerializeField] private InputActionReference moveAction;

    private Rigidbody2D playerBody;
    private Vector2 moveDirection;

    private void Awake()
    {
        playerBody = GetComponent<Rigidbody2D>();
    }

    private void OnEnable()
    {
        if (moveAction == null || moveAction.action == null)
        {
            Debug.LogError("Move Action is not assigned.", this);
            enabled = false;
            return;
        }

        moveAction.action.Enable();
    }

    private void Update()
    {
        // Read arrow-key input and normalize diagonal movement.
        moveDirection = moveAction.action
            .ReadValue<Vector2>().normalized;
    }

    private void FixedUpdate()
    {
        // Move through the physics system to respect walls.
        playerBody.linearVelocity = moveDirection * moveSpeed;
    }

    private void OnDisable()
    {
        if (moveAction != null && moveAction.action != null)
        {
            moveAction.action.Disable();
        }

        if (playerBody != null)
        {
            playerBody.linearVelocity = Vector2.zero;
        }
    }
}
